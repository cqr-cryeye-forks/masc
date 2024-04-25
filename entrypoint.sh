#!/usr/bin/env bash
cmd="$@"

echo python3 masc.py ${cmd}

if [ -n "$http_proxy" ]; then
  sed -i "s/socks4 	127.0.0.1 9050/#socks4    127.0.0.1 9050/" /etc/proxychains4.conf
  sed -i "s/#quiet_mode/quiet_mode/" /etc/proxychains4.conf
  sed -i "s/proxy_dns/#proxy_dns/" /etc/proxychains4.conf
  proxy=$(echo $http_proxy | sed -e 's|^[^/]*//||' -e 's|/.*$||' | cut -f1 -d":")
  echo "http  $proxy 8080" >> /etc/proxychains4.conf
  unset http_proxy
  unset https_proxy
  proxychains4 python3 masc.py ${cmd}

else
  python3 masc.py ${cmd}
fi

