Merhabalar yazdığım aracı kısaca özetliyeyim. Pentest sırasında bir windows cihazın, cihaz ile alakalı bilgileri bize getirmektedir.
Getirmiş olduğu veriler,

Ana makine adı

İşletim Sistemi Adı, Mimarisi ve Sürümü

Makinedeki Kullanıcıların Listesi

Kurulu Yazılım Envanteri

Proxy Ayarlarının Yapılandırılması

Kaydedilen PuTTY Oturumları Kataloğu

Son PuTTY Oturumlarının Kaydı

PuTTY SSH Anahtarlarının Saklanması

Geçmiş Uzak Masaüstü Protokolü (RDP) Oturumlarının Geçmişi

Cihazın bağlı olmuş olduğu Uzak Masaüstü Protokolü (RDP)

Önceki Çalıştırma Komutlarının Günlüğü

Yazmış olduğum aracı iki şekilde kullanılabilir. local_windows_enum.py dosyası cihaza girdikten sorna kullanılır ve herhangi bir shell alma durumu yoktur fakat cihaza girmediyseniz ama karşı cihazın bilgilerini 
elde etmek istiyorsanız remote_windows_enum.py dosyasını çalıştırmanız gerekmektedir.

local_windows_enum.py aracını çalıştırmak için "python local_windows_enum.py" komutunu kullanmanız yeterlidir.

![9](https://github.com/meisterlos/Windows_Enum/assets/81145753/81cf43c6-d6e5-46f2-8b74-fc238d8809f4)

Getirmiş olduğu sonuçlar aşağıdaki gibidir.

![2](https://github.com/meisterlos/Windows_Enum/assets/81145753/9f2ef28b-186d-46fe-b72f-0fee590e7fb3)
![1](https://github.com/meisterlos/Windows_Enum/assets/81145753/9b7a812d-d9ff-483f-afb4-2743c63caa10)

remote_windows_enum.py aracını çalıştırmak için kali cihazımızdan "nc -nvlp 4442" yazın ve bir şekilde dosyayı karşı cihazda çalıştırın.

![10](https://github.com/meisterlos/Windows_Enum/assets/81145753/789199f5-6808-43fd-b42d-605e9c228a15)

Veriler C2 sunucunuza başarılı şekilde gönderildi sonucunu gösterdiğinde kali cihazınıza gelen verileri inceleyebilirsiniz. Eğer verileri gönderirken bir problem yaşanırsa 60 saniye sonra tekrar göndermek için deneyecektir.

![11](https://github.com/meisterlos/Windows_Enum/assets/81145753/6a2657d7-caba-4d4e-a9be-fde4d8f11728)

![12](https://github.com/meisterlos/Windows_Enum/assets/81145753/adcd167a-0f62-465f-a689-f5e701fe1dff)



