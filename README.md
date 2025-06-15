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
   pytest
   ```
   - Test raporu `reports/report.html` olarak oluşur.
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

Her adım tamamlandığında Jenkins arayüzünden test raporlarını ve ekran görüntülerini görebilirsiniz. Sorularınız olursa bana ulaşabilirsiniz!
