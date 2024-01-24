# Laporan Proyek Machine Learning - Budi Setiawan

## Project Domain : Ekonomi dan Bisnis

E-Commerce adalah kegiatan jual beli yang dilakukan secara online melalui internet. Kegiatan yang terjadi dalam e-commerce antara lain transaksi perdagangan, pembayaran, dan pertukaran informasi mengenai suatu produk. Dengan kegiatan yang seperti itu, maka user experience dari e-commerce tersebut harus bagus untuk menjaga user tersebut tidak berhenti menggunakan layanan e-commerce atau berpindah ke e-commerce lain. Untuk mencegah user meninggalkan layanan e-commerce, maka perlu diketahui alasan dari kenapa mereka meninggalkan layanan (_Churn_). Berbagai alasan umum kenapa _churn_ ini bisa terjadi antara lain:

- Pelayanan yang buruk.
- Ketidakpuasan terhadap promo yang ada.
- Kualitas produk yang kurang memuaskan.

Dengan mengetahui user yang potensial untuk meninggalkan layanan, maka bisa dilakukan pencegahan lebih dini supaya user tersebut tidak churn. Dari sisi ini, maka model predictive untuk bisa memprediksi user yang potensial untuk _churn_ akan sangat berguna. 

## Bussines Undestanding

Permasalahan yang dimiliki oleh perusahaan e-commerce salah satunya adalah menjaga loyalitas dari user. Jumlah user adalah nilai jual dari suatu e-commerce. Jumlah user yang besar akan mendatangkan banyak keuntungan, seperti pendapatan dari transaksi akan meningkat, mendatangkan investor, dan juga persepsi positif dari masyarakat luas. Inilah yang menyebabkan loyalitas dari user sangatlah penting dalam sektor ini. Pengguna yang churn bisa menjadi tanda bahwa pengguna tidak puas terhadap layanan atau produk e-commerce tersebut. Hal ini akan berdampak pada potensi pendapatan yang bisa dihasilkan dari transaksi pengguna. 

Dampak lebih jauhnya adalah bisa menyebabkan biaya untuk customer aquisition membengkak, sehingga laba bersih yang didapatkan menurun. Customer aquisition adalah strategi untuk menarik pelanggan baru dan menjadikan mereka sebagai user yang aktif bertransaksi. Strategi yang dilakukan antara lain seperti melakukan promo besar-besaran dalam rentang waktu tertentu, menyebarkan iklan promosi secara online, menggandeng influencer untuk pemasaran konten dan masih banyak lagi. Strategi tersebut memerlukan sumber daya uang yang besar sehingga perlu dilakukan dengan teliti dan hati-hati. Artinya, strategi untuk memperoleh user yang baru tidak akan efektif ketika disisi lain user yang churn tidak dilakukan pencegahan.

### Problem Statements

Berdasarkan uraian diatas, rumusan masalah yang perlu dijawab adalah
- Bagaimana cara mengidentifikasi user yang potential akan churn?
- Apa fitur apa yang paling mempengaruhi churn?

### Goals

Berdasarkan rumusan masalah, solusi untuk mengidentifikasi user yang potential akan churn adalah dengan membangun model prediksi untuk melakukan melakukan klasifikasi terhadap pengguna yang berpotensi untuk churn dari aplikasi e-commerce. Selanjutnya, melakukan analisis lanjutan untuk mengetahui fitur apa saja yang paling berkaitan terhadap curn-nya seorang pengguna.

## Data Undestanding

Sumber data bisa dilihat [disini](https://www.kaggle.com/datasets/ankitverma2010/ecommerce-customer-churn-analysis-and-prediction/data). Data memiliki 5630 observasi dan 20 fitur. Fitur atau kolom dari dataset ini memiliki makna sebagai berikut.

- CustomerID,
- Churn : Churn Flag,
- Tenure : Tenure of customer,
- PreferredLoginDevice : Preferred login device of customer,
- CityTier : City tier,
- WarehouseToHome : Distance in between warehouse to home of customer,
- PreferredPaymentMode : Preferred payment method of customer,
- Gender : Gender of customer,
- HourSpendOnApp : Number of hours spend on mobile application or website,
- NumberOfDeviceRegistered : Total number of deceives is registered on particular customer,
- PreferedOrderCat : Preferred order category of customer in last month,
- SatisfactionScore : Satisfactory score of customer on service,
- MaritalStatus : Marital status of customer,
- NumberOfAddress : Total number of added address on particular customer,
- Complain : complaint has been raised in last month,
- OrderAmountHikeFromlastYear : Percentage increases in order from last year,
- CouponUsed : Total number of coupon has been used in last month,
- OrderCount : Total number of orders has been places in last month,
- DaySinceLastOrder : Day Since last order by customer,
- CashbackAmount : Average cashback in last month

Eksploratory Data yang dilakukan pada notebook ini adalah untuk kepentingan modelling. Pemahaman mendasar terhadap data bisa diperoleh dari mengetahui distribusi untuk data numerik dan mengetahui proporsi setiap value untuk variable kategori. Mengetahui distribusi data data dapat dilakukan dengan memvisualisasikan bentuk dari histogram data tersebut. Sedangkan untuk mengetahui proporsi value untuk setiap kolom kategori bisa divisualisasikan dengan countplot. Distribusi akan digunakan sebagai acuan untuk melakukan transformasi variable dan juga untuk menentukan metode feature engineering apa yang akan digunakan.

### Univariate Analysis

Dataset memiliki tipe data numerik dan kategorikal. Untuk fitur bertipe numerik, akan dilakukan plot untuk mencari tau bentuk distribusinya dengan menggunakan histogram. Dataset memiliki 14 fitur numerik dengan bentuk distribusi seperti gambar dibawah.
![histogram_of_numerical_features](https://github.com/AnnurAfgoni/e-commerce-churn/blob/master/images/histogram_of_numerical_features.png)
Kesimpulan yang bisa diperoleh dari histogram diatas adalah:
- Kebanyakan fitur numerik adalah data deskrit (countable).
- Imbalance dataset, terlihat dari jumlah user yang churn jauh lebih sedikit dibanding dengan yang tidak churn.
- Jumlah complain lebih sedikti dibandingkan dengan yang tidak.
- Kepuasan user kebanyakan netral, terbukti dari SatisfactionScore paling banyak diangka 3 dari interval 1-5. Jumlah yang puas dengan nggak puas juga mirip.
- User paling banyak menghabiskan waktu di aplikasi selama 3 jam.
- Jumlah kupon yang dihabiskan user kebanyakan dibawah 10.
- Kebanyakan user akan order kembali tidak lebih dari 20 hari semenjak dia melakukan order sebelumnya.

Jumlah fitur kategori pada dataset ada 5 fitur. Proporsi value untuk setiap fitur kategori bisa dilihat dibawah
![categori_proportion](https://github.com/AnnurAfgoni/e-commerce-churn/blob/master/images/categori_proportion.png)
Jumlah unique value pada fitur kategori tidak ada yang terlalu banyak. Semuanya masih pada tahap bisa diterima. Garis merah pada plot adalah threshold proporsi untuk _rare label_. _Rare Label_ adalah label yang sangat jarang muncul pada fitur kategori. Threshold yang digunakan adalah 0.05, apabila label itu proporsinya dibawah 0.05 maka akan dikategorikan sebagai _rare label_. Berdasarkan grafik tersebut, disimpulkan bahwa tidak ada fitur yang memiliki _Rare Label_.

### Multivariate Analysis

Untuk melihat pengaruh dari fitur numerik terhadap target, bisa dilihat pada visualisasi dibawah
![violinplot](https://github.com/AnnurAfgoni/e-commerce-churn/blob/master/images/num_x_churn.png)
Gambar diatas adalah violinplot. Terlihat bahwa yang perbedaan yang cukup signifikan ada pada fitur `Tenure` dan `Complain`. User yang churn, cenderung waktu tenornya lebih sebentar dibandingkan dengan yang tidak. Pun sama dengan variable complain, proporsi complain yang churn lebih tinggi dibanding dengan yang tidak. ini menandakan bahwa kedua fitur ini adalah _good predictor_. Kesimpulan ini selaras dengan hasil korelasi fitur yang bisa dilihat pada gambar dibawah. 
![corr](https://github.com/AnnurAfgoni/e-commerce-churn/blob/master/images/correlation.png)
Terlihat bahwa ada beberapa fitur yang saling berkorelasi. Seperti fitur `OrderCount` dengan `CouponUsed`, `OrderCount` dengan `DaySinceLastOrder`. Hal ini perlu dicatat karena akan menjadi rujukan dalam penentuan model. Fitur yang saling berkorelasi akan menimbulkan masalah multikolinearitas pada model LogisticRegression.

## Data Preparation

- **Check Duplicate data**
Duplicate data adalah informasi berlebih yang tidak diperlukan. Jika ada, sebaiknya dihapus. Dataset ini tidak memiliki data duplikasi.
- **Handling missing value**
Fitur yang memiliki missing value semuanya adalah fitur numerik. Jumlah missing value untuk semua kolom tidak lebih dari 1% dari jumlah data. Melihat jarak antara nilai median dan mean tidak terlalu signifikan, maka akan dilakukan imputasi dengan nilai mean. Data missing value akan ditambahkan missing indicator untuk mengetahui apakah data yang missing merupakan good predictor atau tidak. Proporsi Missing value bisa dilihat pada tabel dibawah


- **Handling Outlier**
Hampir semua fitur numerik memiliki outlier. Outlier dideteksi dengan menggunakan metode IQR. Karena outlier kebanyakan bersumber dari distribusi data yang skew, maka data yang ada outlier akan dilakukan transformasi/normalisasi ketimbang dilakukan trimming (penghapusan).
- **Handling cardinality dan Rare Labels**
Cardinality adalah data kategorik yang memiliki terlalu banyak unique value. Sedangkan rare labels adalah label dari fitur kategori yang kemunculannya sangat sedikit. Dataset ini memiliki cardinality yang normal dan tidak ada Rare Labels untuk setiap fitur kategori. Threshold yang digunakan untuk menentukan Rare Labels atau adalah 0,05.
- **Variable Encoding**
Data kategori dilakukan encoding dengan metode frequency encoder. Hal ini dilakukan karena cocok untuk kasus ini, semakin besar bobot semakin besar pengaruh label tersebut.
- **Transformasi Variable**
Transformasi variable bisa berarti scaling/normalisasi. Transformasi yang dicoba dalam notebook adalah `LogTransformation` dan `YeoJohnson`. Transformasi dilakukan hanya pada fitur numerik yang jumlah unique value diatas 10 karena kalau dibawah 10 bisa dianggap data kategori yang sudah di encoding. Untuk fitur numerik dengan unique value dibawah 10 dilakukan scaling dengan `MinMaxScaler`. **Perlu diingat bahwa transformasi ini hanya dilakukan untuk model yang sensitif dengan jarak seperti _KNN_ dan _Logistic Regression_**

## Modelling

Model yang diuji untuk dataset ini ada 5 model. Pertama ada model yang sensitif dengan jarak (_KNN_ dan _Logistic Regressien_), kedua ada tree based model (Decision Tree, Random Forest, dan XGBoost Classifier). Pemilihan model dilakukan dengan melakukan training pada setiap model dengan parameter default, hasil _recall_ untuk kedua model tersebut adalah sebagai berikut
![](https://github.com/AnnurAfgoni/e-commerce-churn/blob/master/images/distance_based_model.png)
Model _Logistic Regression_ dan _KNN_ sensitif terhadap jarak atau skala karena model melakukan perhitungan dengan basis Koordinat Eucledian. Sehingga ketika skala datanya berbeda, model akan bisa dalam melakukan prediksi, dimana nilai dengan bobot yang lebih besar akan lebih mempengaruhi model. Perbedaan perlakuan pada data untuk model yang sensitif terhadap jarak dengan _tree based model_ berada pada transformasi variable. Hal ini dikarenakan _tree based model_ akan mengalami penurunan performa jika dilakukan scaling atau transformasi. 

Untuk _tree based model_ hasilnya sebagai berikut.
![](https://github.com/AnnurAfgoni/e-commerce-churn/blob/master/images/tree_based_model.png)

Proses training dilakukan dengan metode cross validasi untuk melihat konsistensi hasil dari model. Model dengan nilai Recall paling tinggi akan dijadikan model utama untuk dilakukan Hyperparameter Tuning. Model yang dipilih adalah XGBoost karena memiliki nilai recall paling tinggi diantara model yang lain, yaitu sebesar --. Setelah dilakukan Hyperparameter tuning didapat nilai recall sebesar -- untuk data training dan -- untuk data test. Best parameter untuk xgboost adalah:

```sh
Best Parameters:  {
    'subsample': 0.8, 
    'n_estimators': 200, 
    'min_child_weight': 1, 
    'max_depth': 7, 
    'learning_rate': 0.2, 
    'colsample_bytree': 0.8
}
```

## Evaluation

Kasus ini adalah contoh dari kasus klasifikasi. Ketika membangun model prediksi dengan dua target, akan ada dua jenis kesalahan ketika kita ingin melakukan evaluasi terhadap hasil prediksi:

- Type I Error : Hasil prediksi positif padahal aslinya negatif.
Konsekuensi untuk error ini adalah kita akan mengklasifikasi pengguna yang sebenarnya churn padahal tidak churn. Hal ini strategi pencegahan churn nantinya akan salah sassaran, yang bisa jadi menimbulkan biaya. 
- Type II Error : Hasil prediksi negatif padahal aslinya positif.
Konsekuensi untuk error ini adalah kita akan mengklasifikasi pengguna yang sebenarnya tidak churn padahal churn. Hal ini akan mengakibatkan kita akan kehilangan pengguna sehingga berdampak pada bisnis e-commerce.

Mengingat pemasukan terbesar dari E-Commerce adalah transaksi dari user, maka Type II Error lebih penting untuk dicegah. Sehingga metric yang digunakan adalah Recall. Recall merupakan metrics pada metode klasifikasi yang menyatakan seberapa besar persentase kejadian pada kelas positif yang berhasil dideteksi. Dalam kasus ini, penggunaan recall artinya kita ingin memprediksi seakurat mungkin orang-orang yang berpotensi untuk churn dengan meminimalkan False Negatif. 

Formula matematis untuk recall adalah: **$$\frac{TP}{TP+FN}$$**. Dari formula matematik tersebut, nilai dari recall sangat dipengaruhi oleh besar kecilnya nilai FN (False Negatif). Sehingga jika kita menginginkan nilai Recall yang besar, maka nilai FN haruslah kecil.
