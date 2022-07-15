from django.shortcuts import render
from stations.models import station
from django.http import HttpResponse
import csv

# Create your views here.
def home_view(request):
    #print(request.headers)
    #return render(request, "home.html", {})
    if request.method == 'GET':
        gas = ""
        station_type = ""
        date = ""
        time = ""
        gas = request.GET.get("gas")
        station_type = request.GET.get("station")
        date = request.GET.get("date")
        time = request.GET.get("time")
        if gas == "" or gas is None:
            gas = "CO"
        if date == "" or date is None:
            if station_type == "" or station_type is None or station_type == "all":
                station_type = "all"
                results = station.objects.raw(
                        """ SELECT 1 as id, lat, longi, gas_measure
                            FROM tfgdata2
                            WHERE gas_name = '"""+ gas +"""' and station_type = 'static'
                            and left (cast(entry_date AS char), 13) =
                                (select left (cast(max(entry_date) AS char), 13)
                	             from tfgdata2
                	             where station_type = 'static')
                            union all
                            SELECT "1" as id, lat, longi, gas_measure
                            FROM tfgdata2
                            WHERE gas_name = '"""+ gas +"""' and station_type = 'dynamic'
                            and left (cast(entry_date AS char), 13) =
                	           (select left (cast(max(entry_date) AS char), 13)
                	              from tfgdata2
                                  where station_type = 'dynamic');"""
                          )
            else:
                results = station.objects.raw(
                        """ SELECT "1" as id, lat, longi, gas_measure
                            FROM tfgdata2
                            WHERE gas_name = '"""+ gas +"""' and station_type = '"""+station_type+"""'
                            and left (cast(entry_date AS char), 13) =
                	           (select left (cast(max(entry_date) AS char), 13)
                	              from tfgdata2
                                  where station_type = '"""+station_type+"""');"""
                          )
        else:
            search_date = date + " " + time[:-3]
            if station_type == "" or station_type is None or station_type == "all":
                station_type = "all"
                query = """ SELECT 1 as id, lat, longi, gas_measure
                    FROM tfgdata2
                    WHERE gas_name = '"""+ gas +"""' and station_type = 'static'
                    and left (cast(entry_date AS char), 13) = '"""+search_date+"""'
                    union all
                    SELECT "1" as id, lat, longi, gas_measure
                    FROM tfgdata2
                    WHERE gas_name = '"""+ gas +"""' and station_type = 'dynamic'
                    and left (cast(entry_date AS char), 13) = '"""+search_date+"""';"""
                print(query)
                results = station.objects.raw(
                        query
                          )
            else:
                query = """ SELECT "1" as id, lat, longi, gas_measure
                    FROM tfgdata2
                    WHERE gas_name = '"""+ gas +"""' and station_type = '"""+station_type+"""'
                    and left (cast(entry_date AS char), 13) = '"""+search_date+"""'"""
                print (query)
                results = station.objects.raw(
                        query
                          )


    return render(request, "home.html", {'gas':gas, 'results':results, 'stationType':station_type})

def download(request):
    response = HttpResponse(content_type='text/csv')
    lat = request.POST.get("inputDetalleLat")
    long = request.POST.get("inputDetalleLong")
    medicion = request.POST.get("inputDetalleWeight")
    gas = request.POST.get("inputDetalleGas")
    query = """SELECT '1' as id, date_measure, hour_measure, gas_name, gas_measure, station_type from tfgdata2 where lat='""" + lat + """' and longi='""" +long+ """' order by entry_date DESC"""
    results = station.objects.raw(query)
    writer = csv.writer(response ,delimiter=';')
    writer.writerow(['date_measure', 'hour_measure', 'gas_name', 'gas_measure', 'station_type'])
    for result in results:
        writer.writerow([result.date_measure,result.hour_measure,result.gas_name,result.gas_measure,result.station_type])
    #return HttpResponse(status=204)
    return response
