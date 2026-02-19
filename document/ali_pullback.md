<!--------------------------------------------------------------------------------- Description --->
# Poolback 4x4
```
Ichimoku Dual Cloud Switch Backtest
```
```
استراتژی پولبک ۴ برابر  
مبتنی بر دو ابر ایچیموکو – تریگر سویچ کومو در تنظیمات استاندارد + فیلتر روند در تنظیمات بزرگ‌تر
```
```
 جهت‌گیری اصلی: دنباله‌رو روند بزرگ (ابر Ichi2) + پولبک کوتاه‌مدت (سویچ ابر Ichi1)
```
```
واحد محاسبه pnl: تفاوت قیمت خام (بدون در نظر گرفتن حجم معامله، اسپرد، کمیسیون یا اسلیپیج)
```



<!--------------------------------------------------------------------------------- Parameters --->
<br><br>

## Parameters

<!----------------name--->
#### name
```
این پارامتر برای تعیین نام استراتژی می‌باشد
```
```python
name='poolback_4x'
```
<!----------------time_frame--->
#### time_frame
```
تایم‌فریم
```
```python
time_frame='m1'
```
<!----------------region--->
#### region
```
برای تعیین نوع تایم می‌باشد
```
```python
region='UTC'
```
<!----------------time_from--->
#### time_from
```
زمان شروع مجاز معامله
```
```python
time_from='00:00:00'
```
<!----------------time_to--->
#### time_to
```
زمان پایان مجاز معامله
```
```python
time_to='21:00:00'
```
<!----------------max_order--->
#### max_order
```
حداکثر پوزیشن همزمان
```
```python
max_order=1
```
<!----------------domain--->
#### domain
```
گرفتن های و لو همه آیتم‌های داخل متغیر پریود برای دومین دامنه گذشته
```
```python
domain=10
```
<!----------------period--->
#### period
```
تعداد کندل دوره‌های مختلف که کندل بر اساس متغیر تایم فریم تعیین می‌شود
```
```python
period = {
    "t1": 9,
    "k1": 26,
    "sb1": 78,
    "t2": 36,
    "k2": 104,
    "sb2": 234
}
```
<!----------------python--->
#### python
```python
params="{'name': 'poolback_4x', 'time_frame': 'm1', 'region': 'UTC', 'time_from': '00:00:00', 'time_to': '21:00:00', 'max_order': 1, 'domain': 10, 'period': {'t1': 9, 'k1': 26, 'sb1': 78, 't2': 36, 'k2': 104, 'sb2': 234}}"
```



<!--------------------------------------------------------------------------------- Actions --->
<br><br>

## Actions

<!----------------average--->
#### average
```
گرفتن های و لوی همه آیتم‌های داخل متغیر پریود
```
```python
average = {}
for key, value in self.period.items():
    high, low = self.box(date=date, count=value, time_frame=self.time_frame)
    average[key] = {"high": high, "low": low , "average": (high+low)/2}
```

<!----------------sa--->
<br>

#### sa
```
محاسبه میانگین تی و کا
```
```python
sa1 = (average['t1']['average'] + average['k1']['average']) / 2
sa2 = (average['t2']['average'] + average['k2']['average']) / 2
```

<!----------------tk--->
<br>

#### tk
```
تنکن و کیجن صعودی ایچی 2
وقتی تنکن بالای کیجن قرار دارد
```
```python
if average['t2']['average'] > average['k2']['average'] :
    tk_up = True
    tk_down = False
else:
    tk_up = False
    tk_down = True
```

<!----------------kumo--->
<br>

#### kumo
```
کوموی نزولی ایچی2
وقتی sa2 بالای sb2 قرار دارد
```
```python
if sa2 > average['sb2']['average'] :
    kumo_up = True
    kumo_down = False
else:
    kumo_up = False
    kumo_down = True
```

<!----------------switch_down--->
<br>

#### switch_down
```
سویچ نزولی کوموی ایچی 1
کلوز قیمت زیر اسپن آ و اسپن بی
بررسی sa1 و sb1 در کندل لایو و کندل گذشته. وقتی در کندل لایو اسپن آ زیر اسپن بی قرار گرفته و در کندل قبل از لایو اسپن آ بالای اسپن بی قرار داشته است. 
اگر در کندل قبل از لایو اسپن آ برابر با اسپن بی بود به کندل قبل از آن یا - 2 می رویم اگر باز هم برابر بود به - 3 و - 4 و... باید به کندلی برسیم که اسپن آ بالای اسپن بی باشد
```
```python

```













<!----------------candel_close--->
<br>

#### candel_close 
```
سسسسس
```
```
action_1: candel_close | price shoro minute
```

<!----------------switch_up_1--->
<br>

#### switch_up_1
```
سسسسس
```
``` 
#sa1 | sb1 
action_1: loop 10 ta 1
action_1: if sa1[1] > average(count["count_sb_1"])
action_1: 
          if sa1[i-1] < average(count["count_sb_1"])
            javab
          else == 
            sa1[i-2] < average(count["count_sb_1"])
```

<!----------------switch_down_1--->
<br>

#### switch_down_1
```
سسسسس
```
```python
#sa1 | sb1 
action_1: loop 10 ta 1
action_1: if sa1[1] < average(count["count_sb_1"])
action_1: 
          if sa1[i-1] > average(count["count_sb_1"])
            javab
          else == 
            sa1[i-2] > average(count["count_sb_1"])
```



<!----------------tk_down--->
<br>

#### tk_down 
```
سسسسس
```
```
action_1: if average(count["count_t_2"]) < average(count["count_k_2"]) 
```

<!----------------switch_up_2--->
<br>

#### switch_up_2
```
سسسسس
```
```
#sa2 | sb2
action_1: loop 10 ta 1
action_1: if sa2[1] > average(count["count_sb_1"])
action_1: 
          if sa1[i-1] < average(count["count_sb_1"])
            javab
          else == 
            sa1[i-2] < average(count["count_sb_1"])
```

<!----------------switch_down_2--->
<br>

#### switch_down_2
```
سسسسس
```
```
#sa2 | sb2
action_1: switch_down_2
action_1: loop 10 ta 1
action_1: if sa1[1] < average(count["count_sb_1"])
action_1: 
          if sa1[i-1] > average(count["count_sb_1"])
            javab
          else == 
            sa1[i-2] > average(count["count_sb_1"])
```

<!----------------enter--->
<br>

#### enter
```
سسسسس
```
```
action_1: if switch_up_2 ** tk_up_2 && switch_down_1
action_2: buy
action_3: if switch_down_2 ** tk_down_2 && switch_up_1
action_4: sell
```


<!--------------------------------------------------------------------------------- Methods --->
<br><br>

## Methods
<!----------------box--->

#### box
```
این متد یک دیت می‌گیرد یک عدد می‌گیرد و یک تایم فریم می‌گیرد و های و لو آن بازه را برای ما برمی‌گرداند
```
```python
  def box(
          self,
          date:int, 
          count:int,
          time_frame:str,
      ):
      #--------------Description
      # IN     : date | count | time_frame
      # OUT    : high | low
      # Action : این متد یک دیت می‌گیرد یک عدد می‌گیرد و یک تایم فریم می‌گیرد و های و لو آن بازه را برای ما برمی‌گرداند
      #--------------Action
      table = get_tbl_name(self.symbol, self.time_frame)
      date_to = date
      date_from = date - timedelta(minutes=count)
      cmd = f"SELECT MAX(askhigh), MIN(asklow) FROM {table} WHERE date>='{date_from}' and date<='{date_to}'"
      result = self.data_sql.db.item(cmd=cmd).data
      high = result[0]
      low = result[1]
      return high, low
```