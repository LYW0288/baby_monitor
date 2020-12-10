# baby_monitor
public中的檔案是網頁用到的檔案，網頁畫面如下：  
![image](https://github.com/bird880702/baby_monitor/blob/main/02.png)  
由於樹梅派已經停止運作，因此畫面並不會更新。  
analysis中的檔案是我們分析時使用的資料，data並沒有全部放上來，只篩選了最後比較有用的數據。  
．linear  
  這是用來分析呼吸和心跳的sum_energy時所使用的資料，我們用一些簡單的機制去判斷這兩個資料能不能被使用。(邏輯回歸、SVM等等...)  
  最後的結果之一如下：  
  ![image](https://github.com/bird880702/baby_monitor/blob/main/03.png)  
  紅色是前方沒人的情況，藍色是前方有人但靜止不動的情況。  
．data  
  這是用來嘗試從chest displacement中分離出呼吸與心跳waveform所用到的data。  
  先輸入stat(0123)用來區分4種狀況的data(空曠、有靜止的人、有在動的人、靜止物體)，再輸入兩個數字去抓data。  
  例如 0 1 0(即空曠的情況下 第一個資料 第一個檔案)的輸出為：  
  ![image](https://github.com/bird880702/baby_monitor/blob/main/01.png)  
  這是從這個data中，利用簡單的butterworth濾波器分離出的呼吸心跳圖。  
VSD中的檔案是我們在樹梅派裡使用的檔案，最終進行讀取分析並上傳資料的是check.py，其餘檔案則是我們實驗過程中進行測試時所使用的檔案。
由於從前面的分析可知，我們可以使用簡單的線性函數去分類三種情況(alert、human、move)。  
分類完之後，再將一些會使用到的數值傳上firebase。
在demo影片的資料夾中，我們使用螢幕錄影與現場錄影兩種方式同步進行，"BABY MONITOR - 網頁.mp4"是demo時網頁的樣子，"demo.mp4"則是demo的情況。