
###################
# VPC 
###################
resource "aws_vpc" "this" {
  for_each             = var.vpc_parameters
  cidr_block           = each.value.cidr_block
  enable_dns_support   = each.value.enable_dns_support
  enable_dns_hostnames = each.value.enable_dns_hostnames
  tags = merge(each.value.tags, {
    Name : each.key
  })
}


###################
# Subnet
###################
resource "aws_subnet" "this" {
  for_each   = var.subnet_parameters
  vpc_id     = aws_vpc.this[each.value.vpc_name].id
  availability_zone = each.value.availability_zone
  cidr_block = each.value.cidr_block
  map_public_ip_on_launch = each.value.map_public_ip_on_launch 
  
  tags = merge(each.value.tags, {
    Name : each.key
  })
}


###################
# InterNet Gateway 
###################
resource "aws_internet_gateway" "this" {
  for_each = var.igw_parameters
  vpc_id   = aws_vpc.this[each.value.vpc_name].id
  tags = merge(each.value.tags, {
    Name : each.key
  })
}


###################
# NAT Gateway
###################
resource "aws_nat_gateway" "this" {
  for_each = var.use_nat_gateway ? var.nat_gateway_params : {}

  allocation_id = aws_eip.this[each.value.eip_name].id
  subnet_id     = aws_subnet.this[each.value.subnet_name].id
}


###################
# Elastic IP 
###################
resource "aws_eip" "this" {
  for_each = var.use_nat_gateway ? var.eip_params : {}

  domain   = each.value.domain
}


####################
# Route Table 
####################
resource "aws_route_table" "this" {
  for_each = var.rt_parameters

  vpc_id   = aws_vpc.this[each.value.vpc_name].id
  tags = merge(each.value.tags, {
    Name : each.key
  })

  dynamic "route" {
    for_each = each.value.routes
    content {
      cidr_block = route.value.cidr_block
      gateway_id = route.value.use_igw ? aws_internet_gateway.this[route.value.gateway_id].id : route.value.use_ng ? aws_nat_gateway.this[route.value.gateway_id].id : route.value.gateway_id
    }
  }
}


##########################
# Route table association 
##########################
resource "aws_route_table_association" "this" {
  for_each       = var.rt_association_parameters
  subnet_id      = aws_subnet.this[each.value.subnet_name].id
  route_table_id = aws_route_table.this[each.value.rt_name].id
}


