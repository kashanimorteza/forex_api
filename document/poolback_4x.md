## Parameters

### Strategy Name

Identifies the unique name of the strategy.

``` yaml
name: poolback_4x
```

------------------------------------------------------------------------

### Time Zone

Defines the reference time standard used by the system.

``` yaml
time: utc
```

------------------------------------------------------------------------

### Trading Window

Specifies when the strategy is allowed to operate.

``` yaml
time_start: 00:00:00
time_end: 21:00:00
```

------------------------------------------------------------------------

### Candle Storage

Number of candles that will be stored for calculations.

``` yaml
save_candle_data: 10
```

------------------------------------------------------------------------

### Indicator Counts

Configuration values used for average and cloud calculations.

``` yaml
count:
  count_t_1: 9
  count_k_1: 26
  count_sb_1: 78
  count_t_2: 36
  count_k_2: 104
  count_sb_2: 234
```

------------------------------------------------------------------------

### Time Frame

Main candle timeframe of the strategy.

``` yaml
time_frame: 1m
```






<!--------------------------------------------------------------------------------- poolback_4x --->
# poolback_4x

<!--------------------------------------------------------------------------------- parameter --->
<br><br>

## parameter

This is the name
```
name: poolback_4x
```

This is the region
```
time: utc
```

This is the time
```
time_start: 00:00:00
time_end: 21:00:00
```

This is the save_candle_data
```
save_candle_data : 10
```

This is the count
```
count : {"count_t_1":9 , "count_k_1":26 , "count_sb_1":78 , "count_t_2":36 , "count_k_2":104 , "count_sb_2":234}
```

This is the time_frame
```
time_frame: 1m
```





Description
```
name: poolback_4x
time: utc
time_start: 00:00:00
time_end: 21:00:00
save_candle_data : 10
count : {"count_t_1":9 , "count_k_1":26 , "count_sb_1":78 , "count_t_2":36 , "count_k_2":104 , "count_sb_2":234}
time_frame: 1m
```

Python
```python
if a>b :
  pass
else
pass
```



<!--------------------------------------------------------------------------------- action --->
<br><br>

## action

### data 
```
action_1: gereftane dataye  tamame item haye count
action_2: mohasebeye average bar ase high va low 
action_3 : average[10] = {"count_t_1":9 , "count_k_1":26 , "count_sb_1":78 , "count_t_2":36 , "count_k_2":104 , "count_sb_2":234 }
```

### average: 
```
action_1: sa1[10]:average = (count_t_1 + count_k_1)/2
action_2: sa2[10]:average = (count_t_2 + count_k_2)/2
```

### candel_close: 
```
action_1: candel_close : price shoro minute
```

### switch_up_1
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

### switch_down_1: 
```
#sa1 | sb1 
action_1: loop 10 ta 1
action_1: if sa1[1] < average(count["count_sb_1"])
action_1: 
          if sa1[i-1] > average(count["count_sb_1"])
            javab
          else == 
            sa1[i-2] > average(count["count_sb_1"])
```

### tk_up: 
```
action_1: if average(count["count_t_2"]) > average(count["count_k_2"]) 
```

### tk_down: 
```
action_1: if average(count["count_t_2"]) < average(count["count_k_2"]) 
```

### switch_up_2:
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

### switch_down_2:
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

### enter
```
action_1: if switch_up_2 ** tk_up_2 && switch_down_1
action_2: buy
action_3: if switch_down_2 ** tk_down_2 && switch_up_1
action_4: sell
```
