import requests
import tldextract
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from bs4 import BeautifulSoup


url_dosyasi = input("URL dosyasının ismini giriniz: ")



def url_chech(url_dosyasi):
    print("URL check işlemi yapılıyor...")
    check_list = ["/wp-json","/license.txt"]
    try:
        url = open(url_dosyasi+".txt", "r+")
        url_list = []
        
        return_200 = []
        return_200_only_domain = []
        for i in url:
            a = i.split("\n")
            url_list.append(a[0])
        
        for i in url_list:
            for a in check_list:
                try:
                    
                    request = requests.get("http://"+i+a,timeout=None,verify=False,allow_redirects=False)
                    
                   
                    print(f"{request.status_code} http://{i}{a}")
                    return_200.append(f"http://{i}{a}")
                    if f"http://{i}" in return_200_only_domain:
                        pass
                    else:
                        return_200_only_domain.append(f"http://{i}")
                except requests.exceptions.Timeout:
                    #print(f"Timeout occurred: http://{i}{a}")
                    pass
                except requests.exceptions.ConnectionError:
                    #print(f"Connection Error: http://{i}{a}")
                    pass
                    
        source_check(return_200_only_domain)
        
        
        
    except FileNotFoundError:
        print(f"{url_dosyasi} dosyası bulunamadı")
    
    

def source_check(only_return_200):
    print("Source Code Check yapılıyor..")
    wp_using = []
    for i in only_return_200:
        try:
            page = requests.get(i, verify=False,timeout=None)
            soup = BeautifulSoup(page.content, 'lxml')
            html_codes = soup.prettify()
            if html_codes.find("WordPress") != -1  or html_codes.find("WP") != -1:
                for tags in soup.find_all("meta"): #Burada meta etiketini çekiyor
                    if (tags.get("name", None) == 'generator'): #name etiketi generator olanı buluyor
                        wordpress_version = tags.get("content", None) #content'i alıyor
                        
                        if(len(wordpress_version) <= 15): #15 karakterden fazla ise 
                            if i in wp_using: #daha önceden wp_using listesine yazıldıysa pas geçiyor
                                 pass
                            else:
                                wp_using.append(f"{i} sitesi Wordpress kullanıyor ve sürümü: {wordpress_version}")

                        else:
                            if i in wp_using:
                                pass
                            else:
                                wp_using.append(i) #yazılmadıysa yazıyor fakat sürümü yazmıyor

                            #burada hem sürümü hem de wordpress kullandığını yazıyor çünkü 15 karakterden az
                            #bir değere sahip.
                
        except requests.exceptions.Timeout:
                #print(f"Timeout occurred: http://{i}{a}")
                pass
        except requests.exceptions.ConnectionError:
                #print(f"Connection Error: http://{i}{a}")
                pass
    using_wp(wp_using)
    
        
        

def using_wp(wp_using):
    file = open("wordpress_kullananlar.txt","w", encoding="utf-8")
    for i in wp_using:
        if len(wp_using) == 0:
            print("Wordpress kullanan website yoktur.")
        else:
            print(f"WordPress Kullanan  Websiteleri: {i}")
            
            file.write(i + "\n")
    

url_chech(url_dosyasi)




