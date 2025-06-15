# Python Selenium UI Testleri için CI/CD Pipeline Dökümantasyonu

## 1. Proje Kurulumu

1. Python 3 ve pip kurulu olmalı.
2. Proje klasöründe sanal ortam oluşturun ve bağımlılıkları yükleyin:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Testleri çalıştırmak için:
   ```sh
   python3 -m unittest test_google.py
   ```
   - Test raporu HTML olarak değil, unittest çıktısı olarak terminalde görünür.
   - Ekran görüntüleri `reports/screenshots/` klasörüne kaydedilir.

## 2. GitHub Entegrasyonu

- Tüm dosyaları yeni bir GitHub reposuna push edin.
- `.gitignore` dosyası gereksiz dosyaları hariç tutar.

## 3. Jenkins Pipeline Kurulumu (Docker ile Otomatik Kurulum)

1. Proje dizininde aşağıdaki Dockerfile ve docker-compose.yml dosyaları olmalı:
   - **Dockerfile:** Jenkins, Python, venv ve gerekli eklentiler (pipeline, git, github, htmlpublisher) otomatik kurulur.
   - **docker-compose.yml:** Jenkins'i kolayca başlatır, port ve volume ayarlarını yapar.
2. Jenkins'i başlatmak için terminalde:
   ```sh
   cd /Users/arda.ozyaman/Documents/cicd_demo
   docker compose up --build
   ```
   - Jenkins arayüzüne http://localhost:8080 ile erişebilirsin.
3. Eğer port 8080 doluysa, docker-compose.yml'de portu değiştirip (ör: 9090:8080) tekrar başlatabilirsin.

## 4. Cloudflare Tunnel ile Dışarıya Açma (macOS için)

- Jenkins'i dışarıya açmak için şu komutu kullan:
  ```sh
  docker run -it --rm \
    cloudflare/cloudflared:latest tunnel --url http://host.docker.internal:8080
  ```
- Bu sayede GitHub webhook'ları ve dış erişim için güvenli bir tünel açılır.

## 5. Pipeline Adımları

- Kodları GitHub’dan çeker.
- Python bağımlılıklarını yükler.
- Testleri pytest ile çalıştırır.
- HTML rapor ve ekran görüntülerini arşivler ve Jenkins arayüzüne yükler.

## 6. PR Tetikleme ve Sonuçların Gösterimi

- GitHub repo ayarlarında Jenkins webhook tanımlayın (`/github-webhook/`).
- Jenkins projesinde "GitHub hook trigger for GITScm polling" aktif olmalı.
- PR açıldığında/güncellendiğinde pipeline otomatik tetiklenir.
- Jenkins build'i "required checks" olarak eklenebilir.
- Başarılı/başarısız durumlar PR üzerinde gösterilir.

## 7. Sık Karşılaşılan Sorunlar ve Çözümleri

- **python3-venv hatası:** Dockerfile ile Jenkins imajını python3-venv yüklü olacak şekilde oluşturun.
- **Port çakışması:** docker-compose.yml'de portu değiştirin.
- **Erişim/izin hatası:**
  - Jenkins container'ında volume klasörlerinin sahipliğini `jenkins` kullanıcısına verin:
    ```sh
    docker exec -u 0 -it <container_id> bash
    chown -R jenkins:jenkins /var/jenkins_home
    exit
    ```
  - Veya host'ta:
    ```sh
    sudo chown -R 1000:1000 /Users/arda.ozyaman/Documents/cicd_demo
    ```

## 8. Son Yapılanlar ve Çözümler (2025)

- **Jenkins Docker imajı Chromium/Selenium için güncellendi:**
  - Gerekli tüm Chromium bağımlılıkları Dockerfile'a eklendi (libgbm1, libdrm2, libxshmfence1, libasound2, libnss3, libxss1, libatk-bridge2.0-0, libgtk-3-0, fonts-liberation, vb.).
  - `chromium` ve `chromium-driver` paketleri yüklendi.
- **Selenium testleri için unittest formatına geçildi:**
  - `test_google.py` artık unittest modülünü kullanıyor.
  - Test, https://useinsider.com/careers adresine gidip "Find your dream job" butonunun varlığını kontrol ediyor.
  - Test başarılı veya başarısız olsa da ekran görüntüsü `reports/screenshots/find_dream_job.png` olarak kaydediliyor.
- **Webdriver-manager kaldırıldı, sistemdeki chromedriver kullanıldı:**
  - Kodda chromedriver olarak `/usr/lib/chromium/chromedriver` veya `/usr/bin/chromedriver` kullanılıyor.
  - Sürüm uyumsuzluğu ve başlatılamama sorunları çözüldü.
- **Jenkins pipeline sorunsuz çalışıyor:**
  - Kod checkout, bağımlılık kurulumu, test çalıştırma ve raporlama adımları problemsiz tamamlanıyor.
- **Testler ve raporlar:**
  - Testler her build'de otomatik çalışıyor.
  - HTML rapor ve ekran görüntüleri Jenkins arayüzünde erişilebilir.
- **pytest kaldırıldı:**
  - Artık testler unittest ile çalıştırılıyor, pytest kullanılmıyor.
  - README ve pipeline adımlarında pytest ile ilgili kısımlar güncellendi.

> Sonuç: Artık Jenkins pipeline'ı ile Selenium/Chromium testleri otomatik ve stabil şekilde çalışıyor. Tüm kurulum ve düzeltmeler README'de özetlenmiştir.
