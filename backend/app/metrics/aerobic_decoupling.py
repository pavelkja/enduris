def compute(activity, streams):

  heartrate = streams.get("heartrate")
  distance = streams.get("distance")
  time = streams.get("time")

  if not heartrate or not distance or not time:
      return None

  n = min(len(heartrate), len(distance), len(time))

  if n < 60:
      return None

  # výpočet speed z distance/time
  speed = []

  for i in range(1, n):
      dt = time[i] - time[i - 1]
      dd = distance[i] - distance[i - 1]

      if dt > 0:
          speed.append(dd / dt)
      else:
          speed.append(0)

  # zkrátíme HR na stejnou délku
  heartrate = heartrate[1:]

  n = min(len(heartrate), len(speed))

  midpoint = n // 2

  hr1 = heartrate[:midpoint]
  hr2 = heartrate[midpoint:]

  sp1 = speed[:midpoint]
  sp2 = speed[midpoint:]

  avg_hr1 = sum(hr1) / len(hr1)
  avg_hr2 = sum(hr2) / len(hr2)

  avg_sp1 = sum(sp1) / len(sp1)
  avg_sp2 = sum(sp2) / len(sp2)

  if avg_hr1 == 0 or avg_hr2 == 0:
      return None

  eff1 = avg_sp1 / avg_hr1
  eff2 = avg_sp2 / avg_hr2

  decoupling = (eff1 - eff2) / eff1

  return {
      "metric_name": "aerobic_decoupling",
      "value": decoupling
  }