def timeBetweem(start,end,time):
    if start <= end:
        return start <= time <= end
    else:
        return start <= time or time <= end