# Azure Terraform Configuration for TCB Trading Card Brain

terraform {
  required_version = ">= 1.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "${var.project_name}-${var.environment}-rg"
  location = var.location

  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

# Virtual Network
resource "azurerm_virtual_network" "main" {
  name                = "${var.project_name}-vnet"
  address_space       = [var.vnet_cidr]
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

# Subnet
resource "azurerm_subnet" "app" {
  name                 = "${var.project_name}-app-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = [var.subnet_cidr]
}

# Network Security Group
resource "azurerm_network_security_group" "app" {
  name                = "${var.project_name}-app-nsg"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  security_rule {
    name                       = "SSH"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "HTTP"
    priority                   = 1002
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "HTTPS"
    priority                   = 1003
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "Flask"
    priority                   = 1004
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "5000"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

# Public IP
resource "azurerm_public_ip" "app" {
  name                = "${var.project_name}-app-pip"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  allocation_method   = "Static"
  sku                 = "Standard"

  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

# Network Interface
resource "azurerm_network_interface" "app" {
  name                = "${var.project_name}-app-nic"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.app.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.app.id
  }

  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

# Associate NSG with NIC
resource "azurerm_network_interface_security_group_association" "app" {
  network_interface_id      = azurerm_network_interface.app.id
  network_security_group_id = azurerm_network_security_group.app.id
}

# Virtual Machine
resource "azurerm_linux_virtual_machine" "app" {
  name                = "${var.project_name}-app-vm"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  size                = var.vm_size
  admin_username      = var.admin_username
  network_interface_ids = [
    azurerm_network_interface.app.id,
  ]

  admin_ssh_key {
    username   = var.admin_username
    public_key = var.ssh_public_key
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Premium_LRS"
    disk_size_gb         = 30
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }

  custom_data = base64encode(templatefile("${path.module}/user-data.sh", {
    environment = var.environment
  }))

  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

# Azure PostgreSQL Database (Optional)
resource "azurerm_postgresql_flexible_server" "main" {
  count               = var.use_postgresql ? 1 : 0
  name                = "${var.project_name}-db-${var.environment}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  version             = "15"
  administrator_login = var.db_username
  administrator_password = var.db_password
  storage_mb          = 32768
  sku_name            = var.db_sku_name

  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

resource "azurerm_postgresql_flexible_server_database" "main" {
  count     = var.use_postgresql ? 1 : 0
  name      = var.db_name
  server_id = azurerm_postgresql_flexible_server.main[0].id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

resource "azurerm_postgresql_flexible_server_firewall_rule" "app" {
  count            = var.use_postgresql ? 1 : 0
  name             = "allow-app-vm"
  server_id        = azurerm_postgresql_flexible_server.main[0].id
  start_ip_address = azurerm_public_ip.app.ip_address
  end_ip_address   = azurerm_public_ip.app.ip_address
}
