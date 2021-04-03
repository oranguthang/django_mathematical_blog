from .models import MiniSetting


def mini_settings(x, default=None):
    res = default
    try:
        val = MiniSetting.objects.get(name=x)
        
        if val.type == 1:
            if val.value == 'True' or val.value == '1':
                res = True
            elif val.value == 'False' or val.value == '0':
                res = False
        elif val.type == 2:
            res = int(val.value)
        elif val.type == 3:
            res = float(val.value)
        elif val.type == 4:
            res = val.value
    
    except Exception as e:
        print("Error! " + str(e))
        res = default
    
    return res
