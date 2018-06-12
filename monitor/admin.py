from django.contrib import admin
# Register your models here.
from monitor import models

class HostAdmin(admin.ModelAdmin):
    list_display =  ('id','name','ip','status')
    filter_horizontal = ('host_group','template')

class TemplateAdmin(admin.ModelAdmin):
    list_display = ("id","name")
    # filter_horizontal = ("item")

class ItemAdmin(admin.ModelAdmin):
    filter_horizontal = ('keys',)
    list_display = ('name','interval')
    #list_select_related = ('items',)
# class TriggerExpressionInline(admin.TabularInline):     #只有反向关联时才能这样做
#     model = models.TriggerExpression

class TriggerAdmin(admin.ModelAdmin):
    list_display = ('name','severity')
    # filter_horizontal = ('expression',)
    # inlines = [TriggerExpressionInline,]        #触发器和触发器表达式反向关联，通过TabularInline在触发器页面显示触发器的表达式

class TriggerExpressionAdmin(admin.ModelAdmin):
    # filter_horizontal = ('keys','function',)
    list_display = ["id",'logic_type','cute',]
    def cute(self, obj):
        for p in obj.function.all():
            return ("%s %s(%s(%s))" %(p.data_calc_func,p.name,p.operator_type,p.threshold))
    cute.short_description = '表达式'
    print(("*****参考：https://stackoverflow.com/questions/18108521/many-to-many-in-list-display-django"))

class FunctionAdmin(admin.ModelAdmin):
    list_display = ('data_calc_type_choices','name','operator_type',)

class ActionAdmin(admin.ModelAdmin):
    list_display = ('name','interval')

class ActionOperationAdmin(admin.ModelAdmin):
    list_display = ('name','step_to','step_from','action_type')

admin.site.register(models.Trigger,TriggerAdmin)
admin.site.register(models.TriggerExpression,TriggerExpressionAdmin)
admin.site.register(models.Action,ActionAdmin)
admin.site.register(models.ActionOperation,ActionOperationAdmin)
admin.site.register(models.Host,HostAdmin)
admin.site.register(models.HostGroup)
admin.site.register(models.Template,TemplateAdmin)
admin.site.register(models.Item,ItemAdmin)
admin.site.register(models.Key)
admin.site.register(models.Function,FunctionAdmin)
admin.site.register(models.UserProfile)