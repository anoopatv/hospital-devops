# Latest Amazon Linux 2023 image kandupidikkunnu
data "aws_ssm_parameter" "al2023" {
  name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64"
}

# Firewall: browser-il ninnu app-ilekku (port 5000) varaan anuvadhikkunnu
resource "aws_security_group" "app_sg" {
  name        = "hospital-token-sg"
  description = "Allow app traffic on port 5000"

  ingress {
    description = "App port"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Server (EC2)
resource "aws_instance" "app" {
  ami                    = data.aws_ssm_parameter.al2023.value
  instance_type          = "t3.micro"
  vpc_security_group_ids = [aws_security_group.app_sg.id]
    iam_instance_profile   = aws_iam_instance_profile.ec2_profile.name

  # server thudangumbol Docker install cheyyunnu
  user_data = <<-EOF
    #!/bin/bash
    dnf install -y docker
    systemctl enable --now docker
  EOF

  tags = {
    Name = "hospital-token-server"
  }
}

# Server-inte public IP kaanikkunnu
output "server_public_ip" {
  value = aws_instance.app.public_ip
}