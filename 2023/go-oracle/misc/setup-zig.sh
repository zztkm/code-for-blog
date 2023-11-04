url=$(curl https://ziglang.org/download/index.json | jq -r '.master."x86_64-linux".tarball')
wget -O zig-linux-x86_64.tar.xz ${url}

mkdir ./zig
tar -Jxvf zig-linux-x86_64.tar.xz -C ./zig

echo ${url}

