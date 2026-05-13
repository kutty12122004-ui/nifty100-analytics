from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Check project status'

    def handle(self, *args, **kwargs):
        self.stdout.write("=" * 50)
        self.stdout.write("📊 NIFTY 100 ANALYTICS - STATUS CHECK")
        self.stdout.write("=" * 50)
        
        try:
            from nifty_api.views import ALL_COMPANIES
            count = len(ALL_COMPANIES)
            self.stdout.write(self.style.SUCCESS(f"✅ Companies in views.py: {count}"))
            
            if count == 0:
                self.stdout.write(self.style.ERROR("⚠️ NO COMPANIES FOUND in views.py!"))
            else:
                self.stdout.write(f"\n📋 First 5 companies:")
                for company in ALL_COMPANIES[:5]:
                    self.stdout.write(f"   - {company['company_name']} ({company['symbol']}) - {company['sector']}")
                    
        except ImportError:
            self.stdout.write(self.style.ERROR("❌ Could not import ALL_COMPANIES from views.py"))
        
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("🌐 LIVE URL: https://nifty100-analytics.onrender.com")
        self.stdout.write("=" * 50)
