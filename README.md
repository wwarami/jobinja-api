# کراولر جابینجا
به کمک این چهار تا خطی که نوشتیم میتونید خیلی راحت آگهی های موجود در وبسایت [جابینجا](https://jobimja.ir) رو کراول کنید و لذت ببرین. <br>
همینطور میتونید با استفاده از API صغیری که ارائه دادیم ابزار های خودتون رو بسازین که دیگه خیلی لذت ببرین.
## نحوه کارکرد
به دوشیوه میتونید از ابزار استفاده کنید.
#### 1- در محیط ترمینال
میتوانید از فایل config.json برای فیلتر کردن نتایج با اضافه کردن استان، دسته بندی و کلمه های کلیدی آگهی هارو فیلتر و کراول کنید. در اینجا هم میتونید فقط لینک آگهی هارو بگیرین و هم میتونید کامل اطلاعات مربوط به هر آگهی رو در بیارین.<br>
**[آموزش استفاده در محیط ترمینال](https://github.com/errornight/jobinja-api#آموزش-استفده-در-محیط-ترمینال)**
#### 2- استفاده از API
**[آموزش استفاده به وسیله API](https://github.com/errornight/jobinja-api#آموزش-استفده-با-API)**

## آموزش استفده در محیط ترمینال
1- در مرحله اول فایل config.json رو باز کنید و در آن اطلاعات جستوجوی مورد نظر تونو وارد کنید. مثل این نمونه:
``` json
{
  "page": 1,
  "keywords": ["جنگو", "پایتون"],
  "locations": ["تهران"],
  "categories": ["وب،‌ برنامه‌نویسی و نرم‌افزار"]
}
```
2- حالا این دستور رو وارد کنید.
``` terminal
python main.py --jobs --config config.json
```
*در این حالت تنها لینک آگهی هارا به شما میدهد. اگر اطلاعات هر آگهی رو هم میخواهید، دستور --detail رو هم اضافه کنید*
``` terminal
python main.py --jobs --config config.json --detail
```

## آموزش استفده با API
در1- این دستور را وارد کنید.
``` terminal
uvicorn api:app --reload
```
2- حالا آدرس http://127.0.0.1:8000/docs را در مرورگر وارد کنید و به کمک ابزار Swagger UI از API استفاده کنید.


# امکاناتی که اضافه اضافه خواهند شد:
1- افزایش سرعت کراولر با اضافه کردن asyncio و استفاده از html پارسری که از asynchronous پشتیبانی کنه.<br>
2- امکان ذخیره اطلاعات کراولر در یک فایل json.
<br>
3- ...


