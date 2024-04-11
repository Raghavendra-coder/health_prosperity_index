from rest_framework.views import APIView
from .models import  YearIndexTable
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
from add_data import populate_data_in_database

# Create your views here.
class GetFinalIndex(APIView):
    """
    This API view will get the data of index saved in database.
    """
    def get(self, request):
        try:
            index_data = YearIndexTable.objects.values("year", "health_prosperity_index")
            if not index_data:
                populate_data_in_database()
                index_data = YearIndexTable.objects.values("year", "health_prosperity_index")
            # Extracting the values into separate lists
            years = [entry["year"] for entry in index_data]
            health_prosperity_index = [entry["health_prosperity_index"] for entry in index_data]

            # Constructing the desired dictionary
            result_dict = {"year": years, "health_prosperity_index": health_prosperity_index}

            response = {
                "success": True,
                "message": "data added successfully",
                "data": result_dict
            }
            status = HTTP_200_OK

        except Exception as e:
            response = {
                "success": False,
                "message": f"ERROR : {e}",
                "data": None
            }
            status = HTTP_500_INTERNAL_SERVER_ERROR
        return Response(response, status=status)

