# Python Selenium UI Testleri için CI/CD Pipeline Dökümantasyonu

## 1. Proje Kurulum

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

## 3. Jenkins Pipeline Kurulumu

1. Jenkins kurun ve aşağıdaki eklentileri yükleyin:
   - GitHub Plugin
   - GitHub Pull Request Builder
   - Pipeline
   - HTML Publisher
2. Jenkins agent'ında Python kurulu olmalı.
3. Jenkins ile GitHub bağlantısı için token/credentials ekleyin.
4. Proje köküne eklenen `Jenkinsfile` ile pipeline oluşturun.

## 4. Pipeline Adımlarıı

- Kodları GitHub’dan çeker.
- Python bağımlılıklarını yükler.
- Testleri pytest ile çalıştırır.
- HTML rapor ve ekran görüntülerini arşivler ve Jenkins arayüzüne yükler.

## 5. PR Tetikleme ve Sonuçların Gösterimi

- GitHub repo ayarlarında Jenkins webhook tanımlayın (`/github-webhook/`).
- Jenkins projesinde "GitHub hook trigger for GITScm polling" aktif olmalı.
- PR açıldığında/güncellendiğinde pipeline otomatik tetiklenir.
- Jenkins build'i "required checks" olarak eklenebilir.
- Başarılı/başarısız durumlar PR üzerinde gösterilir.

---

docker run -it --rm \
  -p 8080:8080 \
  cloudflare/cloudflared:latest tunnel --url http://host.docker.internal:55010

Her adım tamamlandığında, Jenkins arayüzünden test raporlarını ve ekran görüntülerini görebilirsiniz. Sorularınız olursa bana ulaşabilirsiniz!
