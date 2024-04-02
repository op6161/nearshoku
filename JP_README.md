<div id="jp_top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://op6160.xyz">
    <img src="README_contents/apple-touch-icon.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">NearShoku - ニア食</h3>

  <p align="center">
    <!--プロジェクトの説明-->
    NearShoku - ニア食は、設定した条件に基づいて、選択した場所（または現在の場所）の近くのレストランを見つけるためのウェブアプリケーションです。
    <br/>    
    使用されるもの
    <br/>
    Geolocationを使用して現在の位置を取得する
    <br/>
    GoogleMaps APIを使用して選択した位置を取得する
    <br/>
    近くのレストラン情報を検索するためのRecruit-HotpepperAPI
    <br />
  </p>
</div>


<!-- ABOUT THE PROJECT -->
## プロジェクトについて

[![nearshoku-pc](README_contents/pc-index-beforeselect-1.jpeg)](https://op6160.xyz)

このプロジェクトの目的は、ユーザーが現在地の近くにあるさまざまなレストランを簡単に見つけて選択できるようにすることです 。
NearShokuを通じて、ユーザーは便利に食事の場所を決め、さまざまなレストランを探索して新しい味を見つけることができます。

<p align="right">(<a href="#jp_top">トップへ戻る</a>)</p>



### 使用技術
[![Python](https://img.shields.io/badge/Python_3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
[![Django](https://img.shields.io/badge/Django_5.3.0-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap_5.3.3-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![jQuery](https://img.shields.io/badge/jQuery_3.5.1-0769AD?style=for-the-badge&logo=jquery&logoColor=white)](https://jquery.com/)

<p align="right">(<a href="#jp_top">トップへ戻る</a>)</p>



<!-- 使用例 -->
# 使用方法 NearShoku


<!-- index 例 -->
## indexページ
### ※日本国内のみ機能します


![index-contents](README_contents/index contents.png)
① 検索範囲を選択 : [ 300m ~ 3KM ]（デフォルトは300m）
<br/>
② 順番を選択 :
<span style="background-color:blue">距離順で検索</span> / 
<span style="background-color:green">おすすめ順で検索</span>
<br/>
③ 位置を選択 : 位置を選ぶこともできます！
<br/>
④ 提出 !
<br/>

<span style="color:yellow">ⓐ 位置を選択すると、ボタンがアクティブになります
![index-button-be](README_contents/btn-before.png) 
![arrred](README_contents/arrred-40px.png)
![index-button-af](README_contents/btn-after.png)
<br/>
ⓑ例</span>
![index-example](README_contents/index-example.png)
範囲: 2km<br/>
順番: おすすめ順で検索<br/>
位置: 大阪難波
<details>
<summary>
  <span style="color:yellow">
    ⓒ順番の違い
  </span>
</summary>
<br>
<img src="README_contents/result-orderbydis.jpeg" width="45%" height="40%">
<img src="README_contents/result-orderbyrec.jpeg" width="45%" height="40%">
</details>
<p align="right">(<a href="#jp_top">トップへ戻る</a>)</p>



<!-- result 例 -->
## 結果ページ

![result-shopbox](README_contents/result-contents-1.png)
- お店情報 <br/>
① お店サムネイル <br/>
② お店名 <br/>
③ お店ジャンル<br/>
④ お店アクセス<br/>
⑤ ページを選択<br/>
![result-shopbox](README_contents/result-contents-2.png)


<details>
    <summary>
        <span style="color:yellow">
        ⓐ お店ボックス
        </span>
    </summary>

![result-shopbox](README_contents/result-contents-3.png)
お店ボックスをクリックすると、お店の詳細情報にリンクされます
</details>
<p align="right">(<a href="#jp_top">トップへ戻る</a>)</p>


<!-- 詳細ページの例 -->
## 詳細ページ
お店ボックスをクリックすると、お店の詳細が表示されます。

![detail-contents](README_contents/detail-contents-1.png)
- お店情報 <br/>
① お店名 <br/>
② 戻る <br/>
<span style="color:green">
③ お店ジャンル <br/>
</span>
④ お店の営業時間 <br/>
⑤ お店のサムネイル<br/>
⑥ お店アクセス <br/>
<span style="color:#F08080">
   ⑦ お店の場所と住所 <br/>
</span>

<p align="right">(<a href="#jp_top">トップへ戻る</a>)</p>


<!-- お問い合わせ -->
## お問い合わせ

Jeong JaeHoon - sagvd01@gmail.com

プロジェクトリンク: [https://github.com/op6161/nearshoku-project](https://github.com/op6161/nearshoku-project)

<p align="right">(<a href="#jp_top">トップへ戻る</a>)</p>