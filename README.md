# Darling in Docker

This is the source code of the Darling Docker image. This is an experimental feature!

Running desktop software under Docker has inherent challenges. It is up to you to ensure that the container can connect to X11, D-Bus (-> PulseAudio) etc.

## Prerequisites

You still need to [build and install](https://docs.darlinghq.org/build-instructions.html) Darling's Linux kernel module within the host system.

BEWARE: The `darling-dkms` package inside this repository is fake.

Before starting the container, do as root:
```
modprobe darling-mach
```

## Tutorial

Starting a container:

```
docker run -d --name darling1 darlinghq/darling:latest
```

Now you have a container named `darling1` with `launchd` and various daemons running. You can drop into a shell:

```
docker exec -ti darling1 shell
```

You can run various commands:

```
docker exec darling1 shell -c 'uname -a'
```

## Technical Notes

Darling uses a virtual chroot environment under `/usr/libexec/darling`:

* If you bind a volume as `/somewhere`, it will be accessible as `/Volumes/SystemRoot/somewhere`.
* If you bind a volume as `/usr/libexec/darling/somewhere`, it will appear as `/somewhere`.

The base system of the image is Ubuntu. Therefore, if you do this, you will drop into a Linux shell, and NOT into the macOS shell:

```
docker exec -ti darling1 /bin/bash
```

macOS Bash lives as `/usr/libexec/darling/bin/bash`. The `shell` command used in above examples is just a convenience shortcut.
