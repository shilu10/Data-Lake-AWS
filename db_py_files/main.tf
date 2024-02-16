resource "aws_instance" "example_instance" {
  ami           = "ami-0c55b159cbfafe1f0"  # Specify your AMI ID
  instance_type = "t2.micro"

  user_data = <<-EOF
              #!/bin/bash
              sudo su -
              export AWS_ACCESS_KEY_ID="your_access_key_id"
              export AWS_SECRET_ACCESS_KEY="your_secret_access_key"
              echo "Hello from user_data script!" > /home/ubuntu/user_data_output.txt
              EOF

  tags = {
    Name = "example-instance"
  }
}