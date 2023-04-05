#!/bin/bash


function refreshRepository {
  sudo apt-get update -y
  sudo apt-get install -y jstest-gtk
  modprobe uinput
}

function configureOnscreenKeyboard {
  sudo apt-get install onboard -y
}

function configureAWS {
  curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip"
  unzip awscliv2.zip
  sudo ./aws/install --update
  aws configure set aws_access_key_id AKIAWXBPGPIPUIAELAHQ
  aws configure set aws_secret_access_key "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"
  aws configure set region us-east-1
  aws configure set output json
  rm -rf ./aws
  rm ./awcliv2.zip
}

function enableSnapStore {
  sudo apt update
  sudo apt install snapd -y
}


refreshRepository
enableSnapStore
configureAWS
configureOnscreenKeyboard
