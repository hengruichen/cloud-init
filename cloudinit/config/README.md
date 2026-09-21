# Configuration

This directory contains the configuration files used by cloud-init.

## Overview

The configuration is stored in the following files:

- `/etc/cloud/cloud.cfg.d/01-config.cfg` - This is the main configuration file.
  It contains the default settings for cloud-init.
- `/etc/cloud/cloud.cfg.d/02-network.cfg` - This file contains the network
  configuration settings.
- `/etc/cloud/cloud.cfg.d/03-network-config.cfg` - This file contains the
  network configuration settings for the network interface.
- `/etc/cloud/cloud.cfg.d/04-apt-setup.cfg` - This file contains the apt
  configuration settings.
- `/etc/cloud/cloud.cfg.d/05-dpkg.cfg` - This file contains the dpkg
  configuration settings.
- `/etc/cloud/cloud.cfg.d/06-apt-pkgs.cfg` - This file contains the apt
  package configuration settings.
- `/etc/cloud/cloud.cfg.d/07-apt-cacher.cfg` - This file contains the apt
  configuration settings for the apt-cacher-ng server.
- `/etc/cloud/cloud.cfg.d/08-apt-secure.cfg` - This file contains the apt
  configuration settings for the apt-secure package.
- `/etc/cloud/cloud.cfg.d/09-apt-transport-https.cfg` - This file contains the
  apt configuration settings for the apt-transport-https package.
- `/etc/cloud/cloud.cfg.d/10-apt-transport-tar.cfg` - This file contains the apt
  configuration settings for the apt-transport-tar package.
- `/etc/cloud/cloud.cfg.d/11-apt-transport-http.cfg` - This file contains the apt
  configuration settings for the apt-transport-http package.
- `/etc/cloud/cloud.cfg.d/12-apt-transport-ftp.cfg` - This file contains the apt
  configuration settings for the apt-transport-ftp package.
- `/etc/cloud/cloud.cfg.d/13-apt-transport-socks.cfg` - This file contains the apt
  configuration settings for the apt-transport-socks package.
- `/etc/cloud/cloud.cfg.d/14-apt-transport-https.cfg` - This file contains the apt
  configuration settings for the apt-transport-https package.
- `/etc/cloud/cloud.cfg.d/15-apt-transport-tar.cfg` - This file contains the apt
  configuration settings for the apt-transport-tar package.
- `/etc/cloud/cloud.cfg.d/16-apt-transport-http.cfg` - This file contains the apt
  configuration settings for the apt-transport-http package.
- `/etc/cloud/cloud.cfg.d/17-apt-transport-ftp.cfg` - This file contains the apt
  configuration settings for the apt-transport-ftp package.
- `/etc/cloud/cloud.cfg.d/18-apt-transport-socks.cfg` - This file contains the apt
  configuration settings for the apt-transport-socks package.
- `/etc/cloud/cloud.cfg.d/19-apt-transport-https.cfg` - This file contains the apt
  configuration settings for the apt-transport-https package.
- `/etc/cloud/cloud.cfg.d/20-apt-transport-tar.cfg` - This file contains the apt
  configuration settings for the apt-transport-tar package.
- `/etc/cloud/cloud.cfg.d/21-apt-transport-http.cfg` - This file contains the apt
  configuration settings for the apt-transport-http package.
- `/etc/cloud/cloud.cfg.d/22-apt-transport-ftp.cfg` - This file contains the apt
  configuration settings for the apt-transport-ftp package.
- `/etc/cloud/cloud.cfg.d/23-apt-transport-socks.cfg` - This file contains the apt
  configuration settings for the apt-transport-socks package.
- `/etc/cloud/cloud.cfg.d/24-apt-transport-https.cfg` - This file contains the apt
  configuration settings for the apt-transport-https package.
- `/etc/cloud/cloud.cfg.d/25-apt-transport-tar.cfg` - This file contains the apt
  configuration settings for the apt-transport-tar package.
- `/etc/cloud/cloud.cfg.d/26-apt-transport-http.cfg` - This file contains the apt
  configuration settings for the apt-transport-http package.
- `/etc/cloud/cloud.cfg.d/27-apt-transport-ftp.cfg` - This file contains the apt
  configuration settings for the apt-transport-ftp package.
- `/etc/cloud/cloud.cfg.d/28-apt-transport-socks.cfg` - This file contains the apt
  configuration settings for the apt-transport-socks package.
- `/etc/cloud/cloud.cfg.d/29-apt-transport-https.cfg` - This file contains the apt
  configuration settings for the apt-transport-https package.
- `/etc/cloud/cloud.cfg.d/30-apt-transport-tar.cfg` - This file contains the apt
  configuration settings for the apt-transport-tar package.
- `/etc/cloud/cloud.cfg.d/31-apt-transport-http.cfg` - This file contains the apt
  configuration settings for the apt-transport-http package.
- `/etc/cloud/cloud.cfg.d/32-apt-transport-ftp.cfg` - This file contains the apt
  configuration settings for the apt-transport-ftp package.
- `/etc/cloud/cloud.cfg.d/33-apt-transport-socks.cfg` - This file contains the apt
  configuration settings for the apt-transport-socks package.
- `/etc/cloud/cloud.cfg.d/34-apt-transport-https.cfg` - This file contains the apt
  configuration settings for the apt-transport-https package.
- `/etc/cloud/cloud.cfg.d/35-apt-transport-tar.cfg` - This file contains the apt
  configuration settings for the apt-transport-tar package.
- `/etc/cloud/cloud.cfg.d/36-apt-transport-http.cfg` - This file contains the apt
  configuration settings for the apt-transport-http package.
- `/etc/cloud/cloud.cfg.d/37-apt-transport-ftp.cfg` - This file contains the apt
  configuration settings for the apt-transport-ftp package.
- `/etc/cloud/cloud.cfg.d/38-apt-transport-socks.cfg` - This file contains the apt
  configuration settings for the apt-transport-socks package.
- `/etc/cloud/cloud.cfg.d/39-apt-transport-https.cfg` - This file contains the apt
  configuration settings for the apt-transport-https package.
- `/etc/cloud/cloud.cfg.d/40-apt-transport-tar.cfg` - This file contains the apt
  configuration settings for the apt-transport-tar package.
- `/etc/cloud/cloud.cfg.d/41-apt-transport-http.cfg` - This file contains the apt
  configuration settings for the apt-transport-http package.
- `/etc/cloud/cloud.cfg.d/42-apt-transport-ftp.cfg` - This file contains the apt
  configuration settings for the apt-transport-ftp package.
- `/etc/cloud/cloud.cfg.d/43-apt-transport-socks.cfg` - This file contains the apt
  configuration settings for the apt-transport-socks package.
- `/etc/cloud/cloud.cfg.d/44-apt-transport-https.cfg` - This file contains the apt
  configuration settings for the apt-transport-https package.
- `/etc/cloud/cloud.cfg.d/45-apt-transport-tar.cfg` - This file contains the apt
  configuration settings for the apt-transport-tar package.
- `/etc/cloud/cloud.cfg.d/46-apt-transport-http.cfg` - This file contains the apt
  configuration settings for the apt-transport-http package.
- `/etc/cloud/cloud.cfg.d/47-apt-transport-ftp.cfg` - This file contains the apt
  configuration settings for the apt-transport-ftp package.
- `/etc/cloud/cloud.cfg.d/48-apt-transport-socks.cfg` - This file contains the apt
  configuration settings for the apt-transport-socks package.
- `/etc/cloud/cloud.cfg.d/49-apt-transport-https.cfg` - This file contains the apt
  configuration settings for the apt-transport-https package.
- `/etc/cloud/cloud.cfg.d/50-apt-transport-tar.cfg` - This file contains the apt
  configuration settings for the apt-transport-tar package.
- `/etc/cloud/cloud.cfg.d/51-apt-transport-http.cfg` - This file contains the apt
  configuration settings for the apt-transport-http package.
- `/etc/cloud/cloud.cfg.d/52-apt-transport-ftp.cfg` - This file contains the apt
  configuration settings for the apt-transport-ftp package.
- `/etc/cloud/cloud.cfg.d/53-apt-transport-socks.cfg` - This file contains the apt
  configuration settings for the apt-transport-socks package.
- `/etc/cloud/cloud.cfg.d/54-apt-transport-https.cfg` - This file contains the apt
  configuration settings for the apt-transport-https package.
- `/etc/cloud/cloud.cfg.d/55-apt-transport-tar.cfg` - This file contains the apt
  configuration settings for the apt-transport-tar package.
- `/etc/cloud/cloud.cfg.d/56-apt-transport-http.cfg` - This file contains the apt
  configuration settings for the apt-transport-http package.
- `/etc/cloud/cloud.cfg.d/57-apt-transport-ftp.cfg` - This file contains the apt
  configuration settings for the apt-transport-ftp package.
- `/etc/cloud/cloud.cfg.d/58-apt-transport-socks.cfg` - This file contains the apt
  configuration settings for the apt-transport-socks package.
- `/etc/cloud/cloud.cfg.d/59-apt-transport-https.cfg` - This file contains the apt
  configuration settings for the apt-transport-https package.
- `/etc/cloud/cloud.cfg.d/60-apt-transport-tar.cfg` - This file contains the apt
  configuration settings for the apt-transport-tar package.
- `/etc/cloud/cloud.cfg.d/61-apt-transport-http.cfg`