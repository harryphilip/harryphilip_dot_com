from django.test import TestCase
from django.contrib.auth.models import User
from one_hundred_and_one.models import Plan,Activity
from datetime import date
# Create your tests here.

class PlanTestCase(TestCase):
    def setUp(self):
        u = User.objects.create(username="test_user")
        p = Plan.objects.create(start_date=date(2016,1,1), user=u)
        for i in range(1,102):
            Activity.objects.create(plan=p,title=i)
    def _get_plan(self):
        return Plan.objects.get(start_date=date(2016, 1, 1))

    def test_end_date(self):
        plan = self._get_plan()
        end_date = plan.end_date()
        self.assertEqual(end_date, date(2018,9,28))

    def test_days_left(self):
        plan = self._get_plan()
        days_left = plan.days_left(current_date=date(2018,9,26))
        self.assertEqual(days_left,2)

    def test_pct_done(self):
        plan = self._get_plan()
        act = plan.activity_set.all()[1]
        act.completion_date = date(2018,8,10)
        act.save()
        pct_done = plan.pct_done(current_date=date(2018,9,26))
        self.assertAlmostEqual(pct_done,1/101.0)

