/* ========================================
   BIASHARA INTELLIGENCE — Website Scripts
   Professional, corporate, bilingual
   ======================================== */

(function() {
    'use strict';

    // ========== LANGUAGE SYSTEM ==========
    const translations = {
        'en': {
            // Navigation
            'nav.home': 'Home',
            'nav.intelligence': 'Intelligence Products',
            'nav.msaidizi': 'Msaidizi App',
            'nav.about': 'About Us',
            'nav.contact': 'Contact',
            'nav.explore': 'Explore Intelligence',
            'nav.download': 'Download Msaidizi',

            // Hero
            'hero.badge': 'Migori, Kenya — Serving All of Africa',
            'hero.title1': 'Biashara Intelligence',
            'hero.subtitle': 'The Economic Nervous System of Africa\'s Informal Economy',
            'hero.description': '200 million informal workers. $1.3 trillion in output. We make it visible, measurable, and actionable.',
            'hero.stat1': 'Informal Workers',
            'hero.stat2': 'Annual Output (USD)',
            'hero.stat3': 'Unmeasured Economy',
            'hero.cta1': 'Explore Intelligence',
            'hero.cta2': 'Download Msaidizi',

            // Phone mockup
            'phone.greeting': 'Habari, Mama!',
            'phone.subtitle': 'Leo umepata profit ya KES 1,240',
            'phone.sales': 'Mauzo',
            'phone.expenses': 'Gharama',
            'phone.advice': 'Ukiuza mandazi kwa KES 10 badala ya KES 8, utapata 25% zaidi!',

            // What We Do
            'whatwedo.tag': 'What We Do',
            'whatwedo.title': 'Transforming Raw Data Into Economic Intelligence',
            'whatwedo.subtitle': 'Biashara Intelligence transforms raw transaction data from Africa\'s informal economy into actionable economic intelligence.',
            'whatwedo.p1.title': 'Data Collection',
            'whatwedo.p1.desc': 'Msaidizi app runs on 2GB phones. Voice-based input in Swahili. Offline-first architecture. Every transaction becomes a data point.',
            'whatwedo.p2.title': 'Intelligence Generation',
            'whatwedo.p2.desc': 'Cloud AI transforms millions of micro-transactions into market intelligence. Pattern recognition, anomaly detection, and predictive analytics at scale.',
            'whatwedo.p3.title': 'Intelligence Delivery',
            'whatwedo.p3.desc': 'Custom reports, real-time APIs, interactive dashboards. Intelligence delivered in the format your team needs, when they need it.',
            'whatwedo.flow1': 'Workers Use<br>Msaidizi',
            'whatwedo.flow2': 'Data Collected &<br>Anonymized',
            'whatwedo.flow3': 'AI Generates<br>Intelligence',
            'whatwedo.flow4': 'Buyers Access<br>Intelligence',

            // Intelligence Products
            'intel.tag': 'For Buyers',
            'intel.title': 'Economic Intelligence From the Ground Up',
            'intel.subtitle': 'Real-time data from Africa\'s largest economic sector — the informal economy. Intelligence that no satellite, survey, or census can provide.',
            'intel.cta': 'Request a Demo →',
            'intel.cta.main': 'Request a Demo',
            'intel.cta.note': 'Free consultation • No commitment required',

            // FMCG
            'intel.fmcg.title': 'For FMCG Companies',
            'intel.fmcg.tagline': '"Know what dukawallahs sell before your distributors do"',
            'intel.fmcg.f1': 'Real-time demand forecasting from 100,000+ informal markets',
            'intel.fmcg.f2': 'Micro-market pricing intelligence across regions',
            'intel.fmcg.f3': 'Distribution gap analysis — find underserved areas',
            'intel.fmcg.f4': 'Competitor product tracking at kiosk level',

            // Government
            'intel.gov.title': 'For Government',
            'intel.gov.tagline': '"Plan with real data, not estimates"',
            'intel.gov.f1': 'MSME formalization tracking across sectors',
            'intel.gov.f2': 'Tax base estimation for the informal sector',
            'intel.gov.f3': 'Economic activity heatmaps for infrastructure planning',
            'intel.gov.f4': 'Policy impact measurement with ground-truth data',

            // Financial
            'intel.fin.title': 'For Financial Institutions',
            'intel.fin.tagline': '"Lend to the unbanked with confidence"',
            'intel.fin.f1': 'Transaction-based credit scoring for informal workers',
            'intel.fin.f2': 'Business viability assessment from real sales data',
            'intel.fin.f3': 'Insurance risk profiling for micro-enterprises',
            'intel.fin.f4': 'Fraud detection through transaction pattern analysis',

            // Development
            'intel.dev.title': 'For Development Organizations',
            'intel.dev.tagline': '"Measure impact with ground-truth data"',
            'intel.dev.f1': 'Program targeting and evaluation with real economic data',
            'intel.dev.f2': 'Financial inclusion metrics beyond surveys',
            'intel.dev.f3': 'Real-time economic indicators for rapid response',
            'intel.dev.f4': 'SDG tracking with granular, sub-national data',

            // Pricing
            'pricing.title': 'Flexible Pricing Models',
            'pricing.subtitle': 'Choose the model that fits your organization',
            'pricing.sub.title': 'Subscription',
            'pricing.sub.desc': 'Monthly or annual access to intelligence dashboards and reports. Scaled to your needs.',
            'pricing.sub.tag': 'Most Popular',
            'pricing.api.title': 'Per-Query API',
            'pricing.api.desc': 'Pay per API call. Perfect for integrating intelligence into your existing systems.',
            'pricing.api.tag': 'Developer Friendly',
            'pricing.outcome.title': 'Outcome-Based',
            'pricing.outcome.desc': 'Pay for results. We share the risk — you only pay when the intelligence delivers value.',
            'pricing.outcome.tag': 'Risk-Free',
            'pricing.grant.title': 'Grant-Funded',
            'pricing.grant.desc': 'Special pricing for NGOs, research institutions, and development organizations.',
            'pricing.grant.tag': 'Impact Focused',

            // Msaidizi
            'msaidizi.tag': 'For Workers',
            'msaidizi.title': 'Your Business Assistant.<br>Works Offline. Speaks Swahili.',
            'msaidizi.subtitle': 'Msaidizi is free for every informal worker in Africa. Track your business, understand your profits, and grow — all by speaking in Swahili.',
            'msaidizi.f1.title': 'Voice Input in Swahili & Sheng',
            'msaidizi.f1.desc': 'Just speak. "Nimeuza mandazi mia tano" — Msaidizi understands and records it. No typing needed.',
            'msaidizi.f2.title': 'Automatic Profit Tracking',
            'msaidizi.f2.desc': 'See your daily, weekly, and monthly profits automatically. Know if your business is growing.',
            'msaidizi.f3.title': 'Business Advice',
            'msaidizi.f3.desc': 'Get personalized tips based on your business. "Ukiuza asubuhi, utapata wateja zaidi" — real advice from your data.',
            'msaidizi.f4.title': 'WhatsApp Reports',
            'msaidizi.f4.desc': 'Get your business summary on WhatsApp every week. Share with family or your savings group.',
            'msaidizi.f5.title': 'Works Offline',
            'msaidizi.f5.desc': 'No internet? No problem. Record transactions offline, sync when connected. Works on any Android phone.',
            'msaidizi.f6.title': '100% Free. Your Data is Yours.',
            'msaidizi.f6.desc': 'Msaidizi is free forever. Your personal business data stays yours. Only anonymized, aggregated data feeds intelligence products.',
            'msaidizi.download': 'Download APK',
            'msaidizi.download.note': 'Free • 12MB • Android 5.0+',

            // Flywheel
            'flywheel.tag': 'The Data Flywheel',
            'flywheel.title': 'Every Worker Makes Intelligence Better. Every Buyer Makes the Product Better.',
            'flywheel.s1.title': 'Workers Use Msaidizi',
            'flywheel.s1.desc': 'Free app. Voice input. Every informal worker can track their business and get advice.',
            'flywheel.s2.title': 'Transactions Recorded',
            'flywheel.s2.desc': 'Every sale, purchase, and expense becomes a structured data point. Anonymized and aggregated.',
            'flywheel.s3.title': 'Intelligence Generated',
            'flywheel.s3.desc': 'Cloud AI transforms millions of micro-transactions into market intelligence, trends, and predictions.',
            'flywheel.s4.title': 'Buyers Pay for Intelligence',
            'flywheel.s4.desc': 'FMCG, government, banks, and NGOs subscribe to intelligence products and APIs.',
            'flywheel.s5.title': 'Revenue Improves the Product',
            'flywheel.s5.desc': 'Revenue funds better AI, more features, and expansion to more workers and markets.',
            'flywheel.quote': '"Every worker makes the intelligence better. Every buyer makes the product better. The flywheel never stops."',

            // About
            'about.tag': 'About Us',
            'about.title': 'Biashara Intelligence — Migori, Kenya',
            'about.mission.label': 'Our Mission',
            'about.mission': 'To make Africa\'s invisible economy visible, intelligent, and actionable.',
            'about.story.label': 'Our Story',
            'about.story1': 'Started with one question: <strong>Why does my mum\'s business have no data?</strong>',
            'about.story2': 'She sells mandazi in Gikomba. She works harder than any CEO. But no bank sees her. No government counts her. No company studies her market.',
            'about.story3': '<strong>Biashara Intelligence changes that.</strong>',
            'about.story4': 'We built Msaidizi to give every informal worker a voice — literally. A voice-based app that turns daily transactions into data, and data into power. Power to get loans. Power to grow businesses. Power to be counted.',
            'about.story5': 'Today, we\'re building Africa\'s first economic intelligence platform from the ground up — powered by the very workers the economy forgot to measure.',
            'about.v1.title': 'Ground Truth',
            'about.v1.desc': 'We don\'t estimate. We measure. Every data point comes from a real transaction.',
            'about.v2.title': 'Worker-First',
            'about.v2.desc': 'Workers are partners, not data sources. They get free tools. Their data stays theirs.',
            'about.v3.title': 'Rigorous',
            'about.v3.desc': 'Statistical methods. Peer-reviewed. Academic partnerships. Intelligence you can trust.',
            'about.founder.bio': '"I watched my mother run a business for 20 years with no data, no credit, no visibility. I built Biashara Intelligence so that 200 million workers like her can finally be seen."',

            // Contact
            'contact.tag': 'Get In Touch',
            'contact.title': 'Ready to See the Invisible Economy?',
            'contact.subtitle': 'Whether you\'re a business seeking intelligence, a government planning policy, or a worker wanting to grow — we\'d love to hear from you.',
            'contact.form.name': 'Full Name',
            'contact.form.email': 'Email Address',
            'contact.form.org': 'Organization',
            'contact.form.type': 'I\'m interested as...',
            'contact.form.type.fmcg': 'FMCG Company',
            'contact.form.type.gov': 'Government Agency',
            'contact.form.type.bank': 'Financial Institution',
            'contact.form.type.ngo': 'Development Organization / NGO',
            'contact.form.type.research': 'Research Institution',
            'contact.form.type.worker': 'Informal Worker',
            'contact.form.type.other': 'Other',
            'contact.form.message': 'Message',
            'contact.form.submit': 'Send Message',
            'contact.form.success': 'Message Sent!',
            'contact.form.success.desc': 'Thank you for reaching out. We\'ll get back to you within 24 hours.',
            'contact.email': 'Email',
            'contact.whatsapp': 'WhatsApp',
            'contact.location': 'Location',
            'contact.trust': 'Registered in Kenya. Serving businesses, governments, and workers across Africa.',

            // Footer
            'footer.tagline': 'Making Africa\'s Invisible Economy Visible',
            'footer.products': 'Products',
            'footer.intelligence': 'Intelligence Products',
            'footer.msaidizi': 'Msaidizi App',
            'footer.api': 'API Access',
            'footer.dashboards': 'Dashboards',
            'footer.company': 'Company',
            'footer.about': 'About Us',
            'footer.story': 'Our Story',
            'footer.careers': 'Careers',
            'footer.contact': 'Contact',
            'footer.resources': 'Resources',
            'footer.docs': 'Documentation',
            'footer.blog': 'Blog',
            'footer.privacy': 'Privacy Policy',
            'footer.terms': 'Terms of Service'
        },
        'sw': {
            // Navigation
            'nav.home': 'Nyumbani',
            'nav.intelligence': 'Bidhaa za Ujasusi',
            'nav.msaidizi': 'Programu ya Msaidizi',
            'nav.about': 'Kutuhusu',
            'nav.contact': 'Wasiliana',
            'nav.explore': 'Chunguza Ujasusi',
            'nav.download': 'Pakua Msaidizi',

            // Hero
            'hero.badge': 'Migori, Kenya — Tunahudumia Afrika Yote',
            'hero.title1': 'Biashara Intelligence',
            'hero.subtitle': 'Mfumo wa Fashira wa Uchumi wa Afrika Usio Rasmi',
            'hero.description': 'Wafanyakazi milioni 200 wasio rasmi. Pato la dola trilioni 1.3. Tunafanya ionekane, ipimike, na itumike.',
            'hero.stat1': 'Wafanyakazi Wasio Rasmi',
            'hero.stat2': 'Pato la Mwaka (USD)',
            'hero.stat3': 'Uchumi Usiopimwa',
            'hero.cta1': 'Chunguza Ujasusi',
            'hero.cta2': 'Pakua Msaidizi',

            // Phone mockup
            'phone.greeting': 'Habari, Mama!',
            'phone.subtitle': 'Leo umepata profit ya KES 1,240',
            'phone.sales': 'Mauzo',
            'phone.expenses': 'Gharama',
            'phone.advice': 'Ukiuza mandazi kwa KES 10 badala ya KES 8, utapata 25% zaidi!',

            // What We Do
            'whatwedo.tag': 'Tunafanya Nini',
            'whatwedo.title': 'Kubadilisha Data Mbichi Kuwa Ujasusi wa Kiuchumi',
            'whatwedo.subtitle': 'Biashara Intelligence inabadilisha data ya miamala kutoka uchumi usio rasmi wa Afrika kuwa ujasusi wa kiuchumi unaochezewa.',
            'whatwedo.p1.title': 'Kukusanya Data',
            'whatwedo.p1.desc': 'Programu ya Msaidizi inafanya kazi kwenye simu za 2GB. Ingizo la sauti kwa Kiswahili. Muundo wa kwanza nje ya mtandao. Kila miamala inakuwa data.',
            'whatwedo.p2.title': 'Kuzalisha Ujasusi',
            'whatwedo.p2.desc': 'AI ya wingu inabadilisha miamala milioni kuwa ujasusi wa soko. Utambuzi wa mifumo, ugunduzi wa hitilafu, na uchambuzi wa utabiri.',
            'whatwedo.p3.title': 'Kutoa Ujasusi',
            'whatwedo.p3.desc': 'Ripoti maalum, APIs za wakati halisi, dashibodi za maingiliano. Ujasusi unatolewa katika muundo ambao timu yako inahitaji.',
            'whatwedo.flow1': 'Wafanyakazi Wanatumia<br>Msaidizi',
            'whatwedo.flow2': 'Data Inakusanywa na<br>Kufichwa',
            'whatwedo.flow3': 'AI Inazalisha<br>Ujasusi',
            'whatwedo.flow4': 'Wanunuzi Wanapata<br>Ujasusi',

            // Intelligence Products
            'intel.tag': 'Kwa Wanunuzi',
            'intel.title': 'Ujasusi wa Kiuchumi Kutoka Chini',
            'intel.subtitle': 'Data ya wakati halisi kutoka sekta kubwa zaidi ya uchumi wa Afrika — uchumi usio rasmi. Ujasusi ambao hakuna sateliti, utafiti, au sensa unaweza kutoa.',
            'intel.cta': 'Omba Maonyesho →',
            'intel.cta.main': 'Omba Maonyesho',
            'intel.cta.note': 'Ushauri wa bure • Hakuna kibali kinachohitajika',

            // FMCG
            'intel.fmcg.title': 'Kwa Kampuni za FMCG',
            'intel.fmcg.tagline': '"Jua dukawallahs wanauza nini kabla ya wasambazaji wako"',
            'intel.fmcg.f1': 'Utabiri wa mahitaji wa wakati halisi kutoka masoko 100,000+ yasiyo rasmi',
            'intel.fmcg.f2': 'Ujasusi wa bei za masoko madogo katika mikoa',
            'intel.fmcg.f3': 'Uchambuzi wa mapengo ya usambazaji — pata maeneo yasiyohudumiwa',
            'intel.fmcg.f4': 'Ufuatiliaji wa bidhaa za washindani katika kiwango cha kibanda',

            // Government
            'intel.gov.title': 'Kwa Serikali',
            'intel.gov.tagline': '"Panga na data halisi, sio makadirio"',
            'intel.gov.f1': 'Ufuatiliaji wa uwezekano wa MSME katika sekta',
            'intel.gov.f2': 'Makadirio ya msingi wa kodi kwa sekta isiyo rasmi',
            'intel.gov.f3': 'Ramili za shughuli za kiuchumi kwa kupanga miundombinu',
            'intel.gov.f4': 'Kipimo cha athari za sera na data halisi',

            // Financial
            'intel.fin.title': 'Kwa Taasisi za Kifedha',
            'intel.fin.tagline': '"Wazima kwa wasio na akaunti kwa ujasiri"',
            'intel.fin.f1': 'Alama za mkopo kulingana na miamala kwa wafanyakazi wasio rasmi',
            'intel.fin.f2': 'Tathmini ya uwezekano wa biashara kutoka data halisi ya mauzo',
            'intel.fin.f3': 'Wasifu wa hatari za bima kwa biashara ndogo',
            'intel.fin.f4': 'Ugunduzi wa udanganyifu kupitia uchambuzi wa mifumo ya miamala',

            // Development
            'intel.dev.title': 'Kwa Mashirika ya Maendeleo',
            'intel.dev.tagline': '"Kipimo cha athari na data halisi"',
            'intel.dev.f1': 'Kulenga na kutathmini programu na data halisi ya kiuchumi',
            'intel.dev.f2': 'Vipimo vya ujumuishaji wa kifedha zaidi ya utafiti',
            'intel.dev.vi.f3': 'Viashiria vya kiuchumi vya wakati halisi kwa majibu ya haraka',
            'intel.dev.f4': 'Ufuatiliaji wa SDG na data ya ndani ya nchi',

            // Pricing
            'pricing.title': 'Mifumo Bei Inayobadilika',
            'pricing.subtitle': 'Chagua mfano unaofaa shirika lako',
            'pricing.sub.title': 'Usajili',
            'pricing.sub.desc': 'Upatikanaji wa kila mwezi au mwaka wa dashibodi na ripoti za ujasusi.',
            'pricing.sub.tag': 'Maarufu Zaidi',
            'pricing.api.title': 'API ya Kila Swali',
            'pricing.api.desc': 'Lipa kwa kila wito wa API. Bora kwa kuingiza ujasusi katika mifumo yako.',
            'pricing.api.tag': 'Rafiki wa Msanidi',
            'pricing.outcome.title': 'Kulingana na Matokeo',
            'pricing.outcome.desc': 'Lipa kwa matokeo. Tunashiriki hatari — unalipa tu ujasusi unapotoa thamani.',
            'pricing.outcome.tag': 'Bila Hatari',
            'pricing.grant.title': 'Inafadhiliwa na Ruzuku',
            'pricing.grant.desc': 'Bei maalum kwa NGOs, taasisi za utafiti, na mashirika ya maendeleo.',
            'pricing.grant.tag': 'Kuzingatia Athari',

            // Msaidizi
            'msaidizi.tag': 'Kwa Wafanyakazi',
            'msaidizi.title': 'Msaidizi Wako wa Biashara.<br>Inafanya Kazi Nje ya Mtandao. Inazungumza Kiswahili.',
            'msaidizi.subtitle': 'Msaidizi ni bure kwa kila mfanyakazi asiye rasmi Afrika. Fuatilia biashara yako, elewa faida zako, na kua — kwa kuzungumza Kiswahili.',
            'msaidizi.f1.title': 'Ingizo la Sauti kwa Kiswahili na Sheng',
            'msaidizi.f1.desc': 'Tuongee. "Nimeuza mandazi mia tano" — Msaidizi anaielewa na kuiandika. Hakuna uhitaji wa kuandika.',
            'msaidizi.f2.title': 'Ufuatiliaji wa Faida Otomatiki',
            'msaidizi.f2.desc': 'Ona faida zako za kila siku, wiki, na mwezi kiotomatiki. Jua kama biashara yako inakua.',
            'msaidizi.f3.title': 'Ushauri wa Biashara',
            'msaidizi.f3.desc': 'Pata vidokezo maalum kulingana na biashara yako. "Ukiuza asubuhi, utapata wateja zaidi" — ushauri halisi kutoka data yako.',
            'msaidizi.f4.title': 'Ripoti za WhatsApp',
            'msaidizi.f4.desc': 'Pata muhtasari wa biashara yako kwenye WhatsApp kila wiki. Shiriki na familia au kikundi chako cha akiba.',
            'msaidizi.f5.title': 'Inafanya Kazi Nje ya Mtandao',
            'msaidizi.f5.desc': 'Hakuna mtandao? Hakuna tatizo. Andika miamala nje ya mtandao, unganisha unapopatikana. Inafanya kazi kwenye simu yoyote ya Android.',
            'msaidizi.f6.title': '100% Bure. Data Yako Ni Yako.',
            'msaidizi.f6.desc': 'Msaidizi ni bure milele. Data yako ya biashara inabaki yako. Tu data iliyofichwa na kukusanywa ndiyo inayolisha bidhaa za ujasusi.',
            'msaidizi.download': 'Pakua APK',
            'msaidizi.download.note': 'Bure • 12MB • Android 5.0+',

            // Flywheel
            'flywheel.tag': 'Gurudumu la Data',
            'flywheel.title': 'Kila Mfanyakazi Anafanya Ujasusi Bora. Kila Mnunuzi Anafanya Bidhaa Bora.',
            'flywheel.s1.title': 'Wafanyakazi Wanatumia Msaidizi',
            'flywheel.s1.desc': 'Programu bure. Ingizo la sauti. Kila mfanyakazi asiye rasmi anaweza kufuatilia biashara yake na kupata ushauri.',
            'flywheel.s2.title': 'Miamala Inarekodiwa',
            'flywheel.s2.desc': 'Kila mauzo, manunuzi, na gharama inakuwa data iliyoandaliwa. Imefichwa na kukusanywa.',
            'flywheel.s3.title': 'Ujasusi Unazalishwa',
            'flywheel.s3.desc': 'AI ya wingu inabadilisha miamala milioni kuwa ujasusi wa soko, mwelekeo, na utabiri.',
            'flywheel.s4.title': 'Wanunuzi Wanalipa kwa Ujasusi',
            'flywheel.s4.desc': 'FMCG, serikali, benki, na NGOs wanajiandikisha kwa bidhaa za ujasusi na APIs.',
            'flywheel.s5.title': 'Mapato Yanaboresha Bidhaa',
            'flywheel.s5.desc': 'Mapato yanafadhili AI bora, vipengele zaidi, na upanuzi kwa wafanyakazi na masoko zaidi.',
            'flywheel.quote': '"Kila mfanyakazi anafanya ujasusi bora. Kila mnunuzi anafanya bidhaa bora. Gurudumu halisimami."',

            // About
            'about.tag': 'Kutuhusu',
            'about.title': 'Biashara Intelligence',
            'about.mission.label': 'Dhamira Yetu',
            'about.mission': 'Kufanya uchumi usioonekana wa Afrika uonekane, uwe na akili, na utumike.',
            'about.story.label': 'Hadithi Yetu',
            'about.story1': 'Ilianza na swali moja: <strong>Kwa nini biashara ya mama yangu haina data?</strong>',
            'about.story2': 'Anauza mandazi Gikomba. Anafanya kazi kwa bidii zaidi ya mkurugenzi yeyote. Lakini hakuna benki inamuona. Hakuna serikali inamhesabu. Hakuna kampuni inasomo soko lake.',
            'about.story3': '<strong>Biashara Intelligence inabadilisha hilo.</strong>',
            'about.story4': 'Tulijenga Msaidizi kumpa kila mfanyakazi asiye rasmi sauti — kwa maana halisi. Programu ya sauti inayobadilisha miamala ya kila siku kuwa data, na data kuwa nguvu. Nguvu ya kupata mikopo. Nguvu ya kukuza biashara. Nguvu ya kuhesabiwa.',
            'about.story5': 'Leo, tunajenga jukwaa la kwanza la ujasusi wa kiuchumi kutoka chini — linaloendeshwa na wafanyakazi wenyewe ambao uchumi ulisahau kupima.',
            'about.v1.title': 'Ukweli wa Msingi',
            'about.v1.desc': 'Hatuji. Tunapima. Kila data inatoka kwa miamala halisi.',
            'about.v2.title': 'Mfanyakazi Kwanza',
            'about.v2.desc': 'Wafanyakazi ni washirika, sio vyanzo vya data. Wanapata zana bure. Data yao inabaki yao.',
            'about.v3.title': 'Kwa Usahihi',
            'about.v3.desc': 'Mbinu za takwimu. Mapitio ya wenzako. Ushirikiano wa kitaaluma. Ujasusi unaoaminiwa.',
            'about.founder.bio': '"Nilimtazama mama yangu akifanya biashara kwa miaka 20 bila data, bila mkopo, bila kuonekana. Nilijenga Biashara Intelligence ili wafanyakazi milioni 200 kama yake hatimaye waonekane."',

            // Contact
            'contact.tag': 'Wasiliana Nasi',
            'contact.title': 'Tayari Kuona Uchumi Usioonekana?',
            'contact.subtitle': 'Iwe wewe ni biashara inayotafuta ujasusi, serikali inayopanga sera, au mfanyakazi anayetaka kukua — tungependa kusikia kutoka kwako.',
            'contact.form.name': 'Jina Kamili',
            'contact.form.email': 'Anwani ya Barua Pepe',
            'contact.form.org': 'Shirika',
            'contact.form.type': 'Nina nifaa kama...',
            'contact.form.type.fmcg': 'Kampuni ya FMCG',
            'contact.form.type.gov': 'Wakala wa Serikali',
            'contact.form.type.bank': 'Taasisi ya Kifedha',
            'contact.form.type.ngo': 'Shirika la Maendeleo / NGO',
            'contact.form.type.research': 'Taasisi ya Utafiti',
            'contact.form.type.worker': 'Mfanyakazi Asiye Rasmi',
            'contact.form.type.other': 'Nyingine',
            'contact.form.message': 'Ujumbe',
            'contact.form.submit': 'Tuma Ujumbe',
            'contact.form.success': 'Ujumbe Umetumwa!',
            'contact.form.success.desc': 'Asante kwa kuwasiliana. Tutajibu ndani ya masaa 24.',
            'contact.email': 'Barua Pepe',
            'contact.whatsapp': 'WhatsApp',
            'contact.location': 'Mahali',
            'contact.trust': 'Imesajiliwa Kenya. Tunahudumia biashara, serikali, na wafanyakazi kote Afrika.',

            // Footer
            'footer.tagline': 'Kufanya Uchumi Usioonekana wa Afrika Uonekane',
            'footer.products': 'Bidhaa',
            'footer.intelligence': 'Bidhaa za Ujasusi',
            'footer.msaidizi': 'Programu ya Msaidizi',
            'footer.api': 'Upatikanaji wa API',
            'footer.dashboards': 'Dashibodi',
            'footer.company': 'Kampuni',
            'footer.about': 'Kutuhusu',
            'footer.story': 'Hadithi Yetu',
            'footer.careers': 'Kazi',
            'footer.contact': 'Wasiliana',
            'footer.resources': 'Rasilimali',
            'footer.docs': 'Nyaraka',
            'footer.blog': 'Blogu',
            'footer.privacy': 'Sera ya Faragha',
            'footer.terms': 'Masharti ya Huduma'
        }
    };

    // Merge comprehensive Swahili translations from external file
    if (window.SwahiliContent) {
        Object.assign(translations.sw, window.SwahiliContent);
    }

    let currentLang = 'en';

    // ========== DOM READY ==========
    document.addEventListener('DOMContentLoaded', function() {
        initNavigation();
        initLanguageToggle();
        initScrollAnimations();
        initCounterAnimations();
        initContactForm();
        initScrollToTop();
        initDataPointsAnimation();
        initSmoothScroll();
    });

    // ========== NAVIGATION ==========
    function initNavigation() {
        const header = document.getElementById('nav-header');
        const hamburger = document.getElementById('nav-hamburger');
        const overlay = document.getElementById('mobile-nav-overlay');
        const mobileLinks = document.querySelectorAll('.mobile-nav-link');

        // Sticky navigation
        let lastScroll = 0;
        window.addEventListener('scroll', function() {
            const currentScroll = window.pageYOffset;

            if (currentScroll > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }

            // Update active nav link
            updateActiveNavLink();

            lastScroll = currentScroll;
        });

        // Mobile menu toggle
        if (hamburger && overlay) {
            hamburger.addEventListener('click', function() {
                hamburger.classList.toggle('open');
                overlay.classList.toggle('open');
                document.body.style.overflow = overlay.classList.contains('open') ? 'hidden' : '';
            });

            // Close mobile menu on link click
            mobileLinks.forEach(function(link) {
                link.addEventListener('click', function() {
                    hamburger.classList.remove('open');
                    overlay.classList.remove('open');
                    document.body.style.overflow = '';
                });
            });
        }
    }

    function updateActiveNavLink() {
        const sections = document.querySelectorAll('section[id]');
        const navLinks = document.querySelectorAll('.nav-link');
        const scrollY = window.pageYOffset + 100;

        sections.forEach(function(section) {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');

            if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
                navLinks.forEach(function(link) {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === '#' + sectionId) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }

    // ========== LANGUAGE TOGGLE ==========
    function initLanguageToggle() {
        const langToggle = document.getElementById('lang-toggle');
        if (!langToggle) return;

        langToggle.addEventListener('click', function() {
            currentLang = currentLang === 'en' ? 'sw' : 'en';
            applyTranslations();
            langToggle.querySelector('.lang-label').textContent = currentLang.toUpperCase();
        });
    }

    function applyTranslations() {
        const elements = document.querySelectorAll('[data-i18n]');
        elements.forEach(function(el) {
            const key = el.getAttribute('data-i18n');
            if (translations[currentLang] && translations[currentLang][key]) {
                if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                    el.placeholder = translations[currentLang][key];
                } else {
                    el.innerHTML = translations[currentLang][key];
                }
            }
        });
    }

    // ========== SCROLL ANIMATIONS ==========
    function initScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        // Observe elements
        const animateElements = document.querySelectorAll(
            '.pillar-card, .intel-card, .pricing-card, .msaidizi-feature, ' +
            '.fw-step, .value-item, .contact-card, .flow-step, .kenya-stat'
        );

        animateElements.forEach(function(el, index) {
            el.classList.add('fade-in');
            el.style.transitionDelay = (index % 4) * 0.1 + 's';
            observer.observe(el);
        });

        // Section headers
        document.querySelectorAll('.section-header').forEach(function(el) {
            el.classList.add('fade-in');
            observer.observe(el);
        });
    }

    // ========== COUNTER ANIMATIONS ==========
    function initCounterAnimations() {
        const counters = document.querySelectorAll('[data-count]');

        const observerOptions = {
            threshold: 0.5
        };

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        counters.forEach(function(counter) {
            observer.observe(counter);
        });
    }

    function animateCounter(element) {
        const target = parseInt(element.getAttribute('data-count'));
        const duration = 2000;
        const start = 0;
        const startTime = performance.now();

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Easing function
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            const current = Math.floor(start + (target - start) * easeOutQuart);

            element.textContent = current.toLocaleString();

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }

        requestAnimationFrame(update);
    }

    // ========== CONTACT FORM ==========
    function initContactForm() {
        const form = document.getElementById('contact-form');
        const success = document.getElementById('form-success');

        if (!form) return;

        form.addEventListener('submit', function(e) {
            e.preventDefault();

            // Simulate form submission
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<span>Sending...</span>';
            submitBtn.disabled = true;

            setTimeout(function() {
                form.style.display = 'none';
                success.style.display = 'block';

                // Reset after 5 seconds
                setTimeout(function() {
                    form.style.display = 'flex';
                    success.style.display = 'none';
                    form.reset();
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 5000);
            }, 1500);
        });
    }

    // ========== SCROLL TO TOP ==========
    function initScrollToTop() {
        const scrollTopBtn = document.getElementById('scroll-top');

        if (!scrollTopBtn) return;

        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 500) {
                scrollTopBtn.classList.add('visible');
            } else {
                scrollTopBtn.classList.remove('visible');
            }
        });

        scrollTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // ========== DATA POINTS ANIMATION ==========
    function initDataPointsAnimation() {
        const container = document.getElementById('hero-data-points');
        if (!container) return;

        // Create floating data points
        for (let i = 0; i < 20; i++) {
            const point = document.createElement('div');
            point.style.cssText = `
                position: absolute;
                width: ${Math.random() * 4 + 2}px;
                height: ${Math.random() * 4 + 2}px;
                background: var(--gold);
                border-radius: 50%;
                opacity: ${Math.random() * 0.15 + 0.05};
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
                animation: float-particle ${Math.random() * 4 + 4}s infinite ease-in-out;
                animation-delay: ${Math.random() * 4}s;
            `;
            container.appendChild(point);
        }
    }

    // ========== SMOOTH SCROLL ==========
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
            anchor.addEventListener('click', function(e) {
                const targetId = this.getAttribute('href');
                if (targetId === '#') return;

                const target = document.querySelector(targetId);
                if (!target) return;

                e.preventDefault();

                const navHeight = document.getElementById('nav-header').offsetHeight;
                const targetPosition = target.offsetTop - navHeight - 20;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            });
        });
    }

    // ========== DOWNLOAD APK BUTTON ==========
    const downloadBtn = document.getElementById('download-apk-btn');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', function(e) {
            e.preventDefault();
            // In production, this would trigger actual APK download
            alert('Msaidizi APK download would start here.\n\nComing soon to Google Play Store!');
        });
    }

    // ========== KEYBOARD NAVIGATION ==========
    document.addEventListener('keydown', function(e) {
        // ESC to close mobile menu
        if (e.key === 'Escape') {
            const overlay = document.getElementById('mobile-nav-overlay');
            const hamburger = document.getElementById('nav-hamburger');
            if (overlay && overlay.classList.contains('open')) {
                overlay.classList.remove('open');
                hamburger.classList.remove('open');
                document.body.style.overflow = '';
            }
        }
    });

})();
