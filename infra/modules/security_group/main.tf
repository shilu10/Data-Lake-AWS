

resource "aws_security_group" "this" {
  name        = var.security_group_name
  description = var.security_group_description
  vpc_id      = var.vpc_id

  tags = var.tags
}


resource "aws_vpc_security_group_ingress_rule" "this" {
	for_each = var.sg_ingress_parameters

  	security_group_id = aws_security_group.this.id
  	cidr_ipv4         = each.value.cidr_ipv4
  	from_port         = each.value.from_port
  	ip_protocol       = each.value.ip_protocol
  	to_port           = each.value.to_port
}


resource "aws_vpc_security_group_egress_rule" "this" {
	for_each = var.sg_egress_parameters
  	security_group_id = aws_security_group.this.id

  	cidr_ipv4         = each.value.cidr_ipv4
  	ip_protocol       = each.value.ip_protocol
}