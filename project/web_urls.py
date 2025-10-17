from django.urls import path, include
from . import web_views
app_name="website"
urlpatterns = [
    path('login/', web_views.login_view, name='login-view'),
    path('', web_views.index, name='index'),

    path('user', web_views.user_view, name='user-view'),
    path('user/create', web_views.user_create_view, name='user-create-view'),
    path('user/<int:pk>/edit', web_views.user_edit_view, name='user-edit-view'),
    path('user/<int:pk>/delete', web_views.user_delete_view, name='user-delete-view'),
    path("user/<int:pk>/dashboard", web_views.dashboard, name="dashboard"),
    path("user/<int:pk>/payment", web_views.add_worklog, name="add_worklog"),

    path('sale', web_views.sale_view, name='sale-view'),
    path('sale/create', web_views.sale_create_view, name='sale-create-view'),
    path('sale/<int:pk>/edit', web_views.sale_edit_view, name='sale-edit-view'),
    path('sale/<int:pk>/delete', web_views.sale_delete_view, name='sale-delete-view'),

    path('purchase', web_views.purchase_view, name='purchase-view'),
    path('purchase/create', web_views.purchase_create_view, name='purchase-create-view'),
    path('purchase/<int:pk>/edit', web_views.purchase_edit_view, name='purchase-edit-view'),
    path('purchase/<int:pk>/delete', web_views.purchase_delete_view, name='purchase-delete-view'),

    path('analysis', web_views.analysis_view, name='analysis-view'),

    path('report/daily', web_views.report_view, name='report-view'),
    path('download-daily-csv/purchase', web_views.download_purchase_daily_csv, name='download_purchase_daily_csv'),
    path('download-daily-csv/sale', web_views.download_sale_daily_csv, name='download_sale_daily_csv'),

    path('report/monthly', web_views.report_monthly_view, name='report-monthly-view'),
    path('download-monthly-csv/purchase', web_views.download_purchase_monthly_csv, name='download-purchase-monthly-csv'),
    path('download-monthly-csv/sale', web_views.download_sale_monthly_csv, name='download-sale-monthly-csv'),

    path('logout', web_views.logout_view, name='logout-view'),
]