variable "create_ec2" {
  type = bool 
  default = false 
}

variable "ec2_params" {
  type = map(object({
    ami = string 
    instance_type = string 
    tags = map(string)
}))

  default = {
    ec2_1 = {
      ami = "ami-0c55b159cbfafe1f0"
      instance_type = "t2.micro"

      tags = {
        "Name": "Ec2-1"
      }
    }

    ec2_2 = {
      ami = "ami-0c55b159cbfafe1f0"
      instance_type = "t2.micro"

      tags = {
        "Name": "Ec2-2"
      }
    }
  }

  
}

resource "aws_instance" "example_instance" {
  for_each = var.create_ec2 ? var.ec2_params : {}

  ami = each.value.ami 
  instance_type = each.value.instance_type

  tags = each.value.tags
 
}

