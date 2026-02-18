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
time_frame='1min'
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
<!----------------period--->
#### period
```
میانگین ھای و لول های مختلف کندل
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
<!----------------sa--->
#### sa
```
میانگین ھای و لول های مختلف کندل
```
```python
sa1 = (t1 + k1)/2
sa2 = (t2 + k2)/2
```



<!--------------------------------------------------------------------------------- Actions --->
<br><br>

## Actions
<!----------------data--->
#### data 
```
سسسسس
```
```
action_1: gereftane dataye  tamame item haye count
action_2: mohasebeye average bar ase high va low 
action_3 | average[10] = {"count_t_1":9 , "count_k_1":26 , "count_sb_1":78 , "count_t_2":36 , "count_k_2":104 , "count_sb_2":234 }
```

<!----------------average--->
<br>

#### average 
```
سسسسس
```
```
action_1: sa1[10]:average = (count_t_1 + count_k_1)/2
action_2: sa2[10]:average = (count_t_2 + count_k_2)/2
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

<!----------------tk_up--->
<br>

#### tk_up
```
سسسسس
```
```
action_1: if average(count["count_t_2"]) > average(count["count_k_2"]) 
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