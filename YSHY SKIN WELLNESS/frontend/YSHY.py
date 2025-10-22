import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
# The camera feature will require this, we will implement it next
# import cv2
import os # For saving the captured image
import mysql.connector # --- Import MySQL Connector ---
from mysql.connector import Error # --- For error handling ---

# --------------------------------------------------
# PHASE 1: INTERNATIONALIZATION (i18n) & TRANSLATIONS
# --------------------------------------------------

LANGUAGES = {
    'en': {
        'app_title': 'Yshy - Skin Analyzer',
        'search_btn': '🔍  Search',
        'take_photo_btn': 'Take Photo',
        'gallery_btn': 'Choose from Gallery',
        'privacy_btn': 'Privacy',
        'view_appointment_btn': 'View Appointment', # New Button
        'back_btn': '< Back',
        'create_appointment_btn': 'Create Appointment',
        'find_dermatologist_btn': 'Find Dermatologist',
        'scan_title': 'Possible Condition: Psoriasis',
        'scan_confidence': 'Confidence: 54%',
        'scan_image_placeholder': '[ Uploaded Image ]',
        'scan_image_error': '[ Error Loading Image ]',
        'scan_disclaimer': 'This is not a medical diagnosis. Consult a dermatologist for a professional opinion.',
        'scan_treatment_title': 'Treatment Suggestions',
        'scan_treatment_body': ('• Moisturize thick plaques daily\n'
                                '• Moderate sun exposure (with sunscreen)\n'
                                '• Avoid smoking and excess alcohol'),
        'scan_food_title': 'Recommended Foods',
        'scan_food_body': ('• Anti-inflammatory foods (turmeric, leafy greens)\n'
                           '• Lean proteins and whole grains'),
        'scan_otc_title': 'OTC Medicines',
        'scan_otc_body': '• Coal tar shampoo for scalp\n• Salicylic acid ointment',
        'appointment_title': 'Create Appointment',
        'form_name': 'Name:',
        'form_age': 'Age:',
        'form_phone': 'Phone:',
        'form_blood': 'Blood Group:',
        'form_doctor': 'Doctor:',
        'form_submit_btn': 'Submit Report',
        'form_print_btn': 'Print Report',
        'form_success_msg': 'Report Submitted!',
        'form_err_all_fields': 'All fields are required.',
        'form_err_age_number': 'Age must be a number.',
        'form_err_phone_invalid': 'Please enter a valid phone number.',
        'form_success_title': 'Success',
        'form_success_body': 'Report Submitted Successfully!',
        'form_print_err_no_report': 'No report to print. Please submit first.',
        'form_print_err_fail': 'Failed to save report: {e}',
        'form_print_success_body': 'Report saved successfully to:\n{filepath}',
        'db_connection_error': 'Database Connection Error:\n{e}', # DB Error Message
        'db_insert_error': 'Database Insert Error:\n{e}', # DB Error Message
        'db_query_error': 'Database Query Error:\n{e}', # DB Error Message
        'disclaimer_title': '⚠️ DISCLAIMER',
        'disclaimer_body': (
            "The information, results, and recommendations provided through the YSHY App are "
            "based on professional medical consultations and verified by qualified healthcare practitioners. "
            "However, the content and results available on this app are intended for informational and guidance "
            "purposes only and should not replace personalized medical advice, diagnosis, or treatment from your "
            "own healthcare provider.\n\nAll images, personal data, and health-related information you share "
            "through the app are handled with strict confidentiality and secured using advanced data protection "
            "measures. Your data will never be shared, sold, or misused under any circumstances.\n\nBy using the "
            "YSHY App, you acknowledge and agree that the app and its developers are not liable for any decisions "
            "made based on the information provided within the app. Always consult your doctor for any medical "
            "concerns or before making changes to your treatment plan."
            "\n\n--- Privacy Policy ---\n"
            "1. Data Collection: We collect only the images you provide and the results generated.\n"
            "2. Data Usage: Data is used solely to provide and improve the analysis service.\n"
            "3. Data Storage: All data is encrypted at rest and in transit.\n"
            "4. Data Sharing: We do not share your personal data with any third parties.\n"
            "5. User Rights: You may request the deletion of your data at any time."
            "\n\n--- Terms of Service ---\n"
            "By using this app, you agree to the disclaimer above. You agree not to hold the app creators liable "
            "for any medical outcomes. This app is not a substitute for a qualified dermatologist. "
            "Use of this app is at your own risk. The service is provided 'as is' without any warranties."
        ),
        'dermo_title': 'Find Dermatologist',
        'dermo_pincode_label': 'Enter your Pincode:',
        'dermo_search_btn': 'Search',
        'dermo_err_pincode': 'Please enter a valid 6-digit pincode.',
        'dermo_results_title': 'Clinics Near "{pincode}"',
        'dermo_clinic1_name': 'Dr. Gupta\'s Skin Clinic',
        'dermo_clinic1_desc': '123, Main Street - 5km away',
        'dermo_clinic2_name': 'Agarwal Derma Care',
        'dermo_clinic2_desc': '45, Old Road - 8km away',
        'dermo_clinic3_name': 'Sharma Skin Care', # New Clinic
        'dermo_clinic3_desc': '78, Park Avenue - 10km away', # New Clinic
        'dermo_clinic4_name': 'Modern Dermatology', # New Clinic
        'dermo_clinic4_desc': 'Block C, Tech Park - 12km away', # New Clinic
        'view_appt_title': 'View Your Appointment', # New Screen Title
        'view_appt_name_label': 'Enter Name:', # New Screen Label
        'view_appt_find_btn': 'Find Appointment', # New Screen Button
        'view_appt_not_found': 'No appointment found for "{name}".', # New Screen Message
        # Updated to show more details from DB
        'view_appt_found': 'Appointment for {name}:\nAge: {age}\nPhone: {phone}\nBlood Group: {blood}\nDoctor: {doctor}',
    },
    'hi': {
        'app_title': 'Yshy - स्किन एनालाइजर',
        'search_btn': '🔍  खोजें',
        'take_photo_btn': 'तस्वीर लें',
        'gallery_btn': 'गैलरी से चुनें',
        'privacy_btn': 'गोपनीयता',
        'view_appointment_btn': 'अपॉइंटमेंट देखें', # New Button
        'back_btn': '< वापस',
        'create_appointment_btn': 'अपॉइंटमेंट बनाएं',
        'find_dermatologist_btn': 'त्वचा विशेषज्ञ खोजें',
        'scan_title': 'संभावित स्थिति: सोरायसिस',
        'scan_confidence': 'आत्मविश्वास: 54%',
        'scan_image_placeholder': '[ अपलोड की गई छवि ]',
        'scan_image_error': '[ छवि लोड करने में त्रुटि ]',
        'scan_disclaimer': 'यह एक चिकित्सा निदान नहीं है। पेशेवर राय के लिए त्वचा विशेषज्ञ से सलाह लें।',
        'scan_treatment_title': 'उपचार के सुझाव',
        'scan_treatment_body': ('• मोटी पट्टिकाओं को प्रतिदिन मॉइस्चराइज़ करें\n'
                                '• मध्यम धूप (सनस्क्रीन के साथ)\n'
                                '• धूम्रपान और अत्यधिक शराब से बचें'),
        'scan_food_title': 'अनुशंसित खाद्य पदार्थ',
        'scan_food_body': ('• सूजन-रोधी खाद्य पदार्थ (हल्दी, पत्तेदार साग)\n'
                           '• लीन प्रोटीन और साबुत अनाज'),
        'scan_otc_title': 'ओटीसी दवाएं',
        'scan_otc_body': '• स्कैल्प के लिए कोल टार शैम्पू\n• सैलिसिलिक एसिड मरहम',
        'appointment_title': 'अपॉइंटमेंट बनाएं',
        'form_name': 'नाम:',
        'form_age': 'उम्र:',
        'form_phone': 'फ़ोन:',
        'form_blood': 'ब्लड ग्रुप:',
        'form_doctor': 'डॉक्टर:',
        'form_submit_btn': 'रिपोर्ट जमा करें',
        'form_print_btn': 'रिपोर्ट प्रिंट करें',
        'form_success_msg': 'रिपोर्ट जमा हो गई!',
        'form_err_all_fields': 'सभी फ़ील्ड आवश्यक हैं।',
        'form_err_age_number': 'उम्र एक संख्या होनी चाहिए।',
        'form_err_phone_invalid': 'कृपया एक मान्य फ़ोन नंबर दर्ज करें।',
        'form_success_title': 'सफलता',
        'form_success_body': 'रिपोर्ट सफलतापूर्वक जमा की गई!',
        'form_print_err_no_report': 'प्रिंट करने के लिए कोई रिपोर्ट नहीं है। कृपया पहले जमा करें।',
        'form_print_err_fail': 'रिपोर्ट सहेजने में विफल: {e}',
        'form_print_success_body': 'रिपोर्ट सफलतापूर्वक यहाँ सहेजी गई:\n{filepath}',
        'db_connection_error': 'डेटाबेस कनेक्शन त्रुटि:\n{e}', # DB Error Message
        'db_insert_error': 'डेटाबेस प्रविष्टि त्रुटि:\n{e}', # DB Error Message
        'db_query_error': 'डेटाबेस क्वेरी त्रुटि:\n{e}', # DB Error Message
        'disclaimer_title': '⚠️ अस्वीकरण',
        'disclaimer_body': (
            "YSHY ऐप के माध्यम से प्रदान की गई जानकारी, परिणाम और सिफारिशें "
            "पेशेवर चिकित्सा परामर्श पर आधारित हैं और योग्य स्वास्थ्य सेवा चिकित्सकों द्वारा सत्यापित हैं। "
            "हालांकि, इस ऐप पर उपलब्ध सामग्री और परिणाम केवल सूचनात्मक और मार्गदर्शन "
            "उद्देश्यों के लिए हैं और इन्हें आपके अपने स्वास्थ्य सेवा प्रदाता से व्यक्तिगत चिकित्सा सलाह, "
            "निदान या उपचार का स्थान नहीं लेना चाहिए।\n\nआपके द्वारा ऐप के माध्यम से साझा की जाने वाली सभी छवियां, "
            "व्यक्तिगत डेटा और स्वास्थ्य संबंधी जानकारी को सख्त गोपनीयता के साथ संभाला जाता है और उन्नत डेटा सुरक्षा "
            "उपायों का उपयोग करके सुरक्षित किया जाता है। आपका डेटा कभी भी किसी भी परिस्थिति में साझा, बेचा या "
            "दुरुपयोग नहीं किया जाएगा।\n\nYSHY ऐप का उपयोग करके, आप स्वीकार करते हैं और सहमत होते हैं कि ऐप "
            "और इसके डेवलपर्स ऐप के भीतर प्रदान की गई जानकारी के आधार पर लिए गए किसी भी निर्णय के लिए उत्तरदायी "
            "नहीं हैं। किसी भी चिकित्सा संबंधी चिंता के लिए या अपनी उपचार योजना में बदलाव करने से पहले हमेशा "
            "अपने डॉक्टर से सलाह लें।"
            "\n\n--- गोपनीयता नीति ---\n"
            "1. डेटा संग्रह: हम केवल आपके द्वारा प्रदान की गई छवियों और उत्पन्न परिणामों को एकत्र करते हैं।\n"
            "2. डेटा उपयोग: डेटा का उपयोग केवल विश्लेषण सेवा प्रदान करने और सुधारने के लिए किया जाता है।\n"
            "3. डेटा भंडारण: सभी डेटा को आराम और पारगमन में एन्क्रिप्ट किया जाता है।\n"
            "4. डेटा साझाकरण: हम आपका व्यक्तिगत डेटा किसी तीसरे पक्ष के साथ साझा नहीं करते हैं।\n"
            "5. उपयोगकर्ता के अधिकार: आप किसी भी समय अपने डेटा को हटाने का अनुरोध कर सकते हैं।"
            "\n\n--- सेवा की शर्तें ---\n"
            "इस ऐप का उपयोग करके, आप उपरोक्त अस्वीकरण से सहमत होते हैं। आप ऐप निर्माताओं को किसी भी "
            "चिकित्सा परिणाम के लिए उत्तरदायी नहीं ठहराने के लिए सहमत हैं। यह ऐप एक योग्य त्वचा विशेषज्ञ "
            "का विकल्प नहीं है। इस ऐप का उपयोग आपके अपने जोखिम पर है। सेवा 'जैसा है' के आधार पर "
            "बिना किसी वारंटी के प्रदान की जाती है।"
        ),
        'dermo_title': 'त्वचा विशेषज्ञ खोजें',
        'dermo_pincode_label': 'अपना पिनकोड दर्ज करें:',
        'dermo_search_btn': 'खोजें',
        'dermo_err_pincode': 'कृपया 6 अंकों का वैध पिनकोड दर्ज करें।',
        'dermo_results_title': '"{pincode}" के पास के क्लिनिक',
        'dermo_clinic1_name': 'डॉ. गुप्ता की त्वचा क्लिनिक',
        'dermo_clinic1_desc': '123, मेन स्ट्रीट - 5 किमी दूर',
        'dermo_clinic2_name': 'अग्रवाल डर्मा केयर',
        'dermo_clinic2_desc': '45, ओल्ड रोड - 8 किमी दूर',
        'dermo_clinic3_name': 'शर्मा स्किन केयर', # New Clinic
        'dermo_clinic3_desc': '78, पार्क एवेन्यू - 10 किमी दूर', # New Clinic
        'dermo_clinic4_name': 'मॉडर्न डर्मेटोलॉजी', # New Clinic
        'dermo_clinic4_desc': 'ब्लॉक सी, टेक पार्क - 12 किमी दूर', # New Clinic
        'view_appt_title': 'अपना अपॉइंटमेंट देखें', # New Screen Title
        'view_appt_name_label': 'नाम दर्ज करें:', # New Screen Label
        'view_appt_find_btn': 'अपॉइंटमेंट खोजें', # New Screen Button
        'view_appt_not_found': '"{name}" के लिए कोई अपॉइंटमेंट नहीं मिला।', # New Screen Message
        # Updated to show more details from DB
        'view_appt_found': '{name} के लिए अपॉइंटमेंट:\nउम्र: {age}\nफ़ोन: {phone}\nब्लड ग्रुप: {blood}\nडॉक्टर: {doctor}',
    },
    'ta': {
        'app_title': 'Yshy - தோல் பகுப்பாய்வி',
        'search_btn': '🔍  தேடு',
        'take_photo_btn': 'புகைப்படம் எடு',
        'gallery_btn': 'கேலரியில் இருந்து தேர்ந்தெடு',
        'privacy_btn': 'தனியுரிமை',
        'view_appointment_btn': 'சந்திப்பைக் காண்க', # New Button
        'back_btn': '< பின்செல்',
        'create_appointment_btn': 'சந்திப்பை உருவாக்கு',
        'find_dermatologist_btn': 'தோல் மருத்துவரைத் தேடு',
        'scan_title': 'சாத்தியமான நிலை: சொரியாசிஸ்',
        'scan_confidence': 'நம்பிக்கை: 54%',
        'scan_image_placeholder': '[ பதிவேற்றப்பட்ட படம் ]',
        'scan_image_error': '[ படத்தை ஏற்றுவதில் பிழை ]',
        'scan_disclaimer': 'இது மருத்துவ निदानம் அல்ல. தொழில்முறை கருத்துகளுக்கு தோல் மருத்துவரை அணுகவும்.',
        'scan_treatment_title': 'சிகிச்சை ஆலோசனைகள்',
        'scan_treatment_body': ('• தடிமனான பிளேக்குகளை தினமும் ஈரப்பதமாக்குங்கள்\n'
                                '• மிதமான சூரிய ஒளி (சன்ஸ்கிரீனுடன்)\n'
                                '• புகைபிடித்தல் மற்றும் அதிக மது அருந்துவதைத் தவிர்க்கவும்'),
        'scan_food_title': 'பரிந்துரைக்கப்பட்ட உணவுகள்',
        'scan_food_body': ('• அழற்சி எதிர்ப்பு உணவுகள் (மஞ்சள், இலை கீரைகள்)\n'
                           '• ஒல்லியான புரதங்கள் மற்றும் முழு தானியங்கள்'),
        'scan_otc_title': 'OTC மருந்துகள்',
        'scan_otc_body': '• உச்சந்தಲೆக்கு கோல் டார் ஷாம்பு\n• சாலிசிலிக் அமில களிம்பு',
        'appointment_title': 'சந்திப்பை உருவாக்கு',
        'form_name': 'பெயர்:',
        'form_age': 'வயது:',
        'form_phone': 'தொலைபேசி:',
        'form_blood': 'இரத்த வகை:',
        'form_doctor': 'மருத்துவர்:',
        'form_submit_btn': 'அறிக்கையைச் சமர்ப்பி',
        'form_print_btn': 'அறிக்கையை அச்சிடு',
        'form_success_msg': 'அறிக்கை சமர்ப்பிக்கப்பட்டது!',
        'form_err_all_fields': 'அனைத்து புலங்களும் தேவை.',
        'form_err_age_number': 'வயது எண்ணாக இருக்க வேண்டும்.',
        'form_err_phone_invalid': 'சரியான தொலைபேசி எண்ணை உள்ளிடவும்.',
        'form_success_title': 'வெற்றி',
        'form_success_body': 'அறிக்கை வெற்றிகரமாக சமர்ப்பிக்கப்பட்டது!',
        'form_print_err_no_report': 'அச்சிட அறிக்கை இல்லை. முதலில் சமர்ப்பிக்கவும்.',
        'form_print_err_fail': 'அறிக்கையைச் சேமிக்க முடியவில்லை: {e}',
        'form_print_success_body': 'அறிக்கை வெற்றிகரமாக சேமிக்கப்பட்டது:\n{filepath}',
        'db_connection_error': 'தரவுத்தள இணைப்புப் பிழை:\n{e}', # DB Error Message
        'db_insert_error': 'தரவுத்தளத்தில் சேர்க்கும் பிழை:\n{e}', # DB Error Message
        'db_query_error': 'தரவுத்தள வினவல் பிழை:\n{e}', # DB Error Message
        'disclaimer_title': '⚠️ பொறுப்புத் துறப்பு',
        'disclaimer_body': (
            "YSHY செயலி மூலம் வழங்கப்படும் தகவல், முடிவுகள் மற்றும் பரிந்துரைகள் "
            "தொழில்முறை மருத்துவ ஆலோசனைகளை அடிப்படையாகக் கொண்டவை மற்றும் தகுதிவாய்ந்த சுகாதாரப் "
            "பணியாளர்களால் சரிபார்க்கப்பட்டவை. இருப்பினும், இந்த செயலியில் கிடைக்கும் உள்ளடக்கம் மற்றும் "
            "முடிவுகள் தகவல் மற்றும் வழிகாட்டுதல் நோக்கங்களுக்காக மட்டுமே மற்றும் உங்கள் சொந்த "
            "சுகாதார வழங்குநரிடமிருந்து தனிப்பயனாக்கப்பட்ட மருத்துவ ஆலோசனை, निदानம் அல்லது "
            "சிகிச்சையை மாற்றக்கூடாது.\n\nநீங்கள் செயலி மூலம் பகிரும் அனைத்து படங்கள், தனிப்பட்ட தரவு "
            "மற்றும் உடல்நலம் தொடர்பான தகவல்கள் கடுமையான ரகசியத்தன்மையுடன் கையாளப்படுகின்றன மற்றும் "
            "மேம்பட்ட தரவு பாதுகாப்பு நடவடிக்கைகளைப் பயன்படுத்தி பாதுகாக்கப்படுகின்றன. உங்கள் தரவு "
            "எந்தவொரு சூழ்நிலையிலும் பகிரப்படவோ, விற்கப்படவோ அல்லது தவறாகப் பயன்படுத்தப்படவோ மாட்டாது.\n\n"
            "YSHY செயலியைப் பயன்படுத்துவதன் மூலம், செயலியின் டெவலப்பர்கள் செயலியினுள் வழங்கப்படும் "
            "தகவலின் அடிப்படையில் எடுக்கப்படும் எந்தவொரு முடிவுகளுக்கும் பொறுப்பல்ல என்பதை நீங்கள் "
            "அறிந்து ஒப்புக்கொள்கிறீர்கள். எந்தவொரு மருத்துவ கவலைகளுக்கும் அல்லது உங்கள் சிகிச்சைத் "
            "திட்டத்தில் மாற்றங்களைச் செய்வதற்கு முன்பும் எப்போதும் உங்கள் மருத்துவரை அணுகவும்."
            "\n\n--- தனியுரிமைக் கொள்கை ---\n"
            "1. தரவு சேகரிப்பு: நீங்கள் வழங்கும் படங்களையும் உருவாக்கப்பட்ட முடிவுகளையும் மட்டுமே நாங்கள் சேகரிக்கிறோம்.\n"
            "2. தரவு பயன்பாடு: பகுப்பாய்வு சேவையை வழங்கவும் மேம்படுத்தவும் மட்டுமே தரவு பயன்படுத்தப்படுகிறது.\n"
            "3. தரவு சேமிப்பு: எல்லா தரவும் ஓய்விலும் பரிமாற்றத்திலும் குறியாக்கம் செய்யப்படுகிறது.\n"
            "4. தரவு பகிர்வு: உங்கள் தனிப்பட்ட தரவை நாங்கள் எந்த மூன்றாம் தரப்பினருடனும் பகிர்ந்து கொள்வதில்லை.\n"
            "5. பயனர் உரிமைகள்: உங்கள் தரவை எந்த நேரத்திலும் நீக்கக் கோரலாம்."
            "\n\n--- சேவை விதிமுறைகள் ---\n"
            "இந்த செயலியைப் பயன்படுத்துவதன் மூலம், மேலே உள்ள பொறுப்புத் துறப்பை நீங்கள் ஒப்புக்கொள்கிறீர்கள். "
            "எந்தவொரு மருத்துவ விளைவுகளுக்கும் செயலி உருவாக்குநர்களைப் பொறுப்பாக்க மாட்டீர்கள் என்று "
            "ஒப்புக்கொள்கிறீர்கள். இந்த செயலி தகுதிவாய்ந்த தோல் மருத்துவருக்கு மாற்றாக இல்லை. "
            "இந்த செயலியைப் பயன்படுத்துவது உங்கள் சொந்த ஆபத்தில் உள்ளது. சேவையானது 'உள்ளபடியே' "
            "எந்தவொரு உத்தரவாதமும் இல்லாமல் வழங்கப்படுகிறது."
        ),
        'dermo_title': 'தோல் மருத்துவரைத் தேடு',
        'dermo_pincode_label': 'உங்கள் பின்கோடை உள்ளிடவும்:',
        'dermo_search_btn': 'தேடு',
        'dermo_err_pincode': 'சரியான 6 இலக்க பின்கோடை உள்ளிடவும்.',
        'dermo_results_title': '"{pincode}" அருகில் உள்ள கிளினிக்குகள்',
        'dermo_clinic1_name': 'டாக்டர் குப்தாவின் தோல் மருத்துவமனை',
        'dermo_clinic1_desc': '123, மெயின் ஸ்ட்ரீட் - 5 கிமீ தொலைவில்',
        'dermo_clinic2_name': 'அகர்வால் டெர்மா கேர்',
        'dermo_clinic2_desc': '45, பழைய சாலை - 8 கிமீ தொலைவில்',
        'dermo_clinic3_name': 'சர்மா ஸ்கின் கேர்', # New Clinic
        'dermo_clinic3_desc': '78, பார்க் அவென்யூ - 10 கிமீ தொலைவில்', # New Clinic
        'dermo_clinic4_name': 'நவீன டெர்மட்டாலஜி', # New Clinic
        'dermo_clinic4_desc': 'பிளாக் சி, டெக் பார்க் - 12 கிமீ தொலைவில்', # New Clinic
        'view_appt_title': 'உங்கள் சந்திப்பைக் காண்க', # New Screen Title
        'view_appt_name_label': 'பெயரை உள்ளிடவும்:', # New Screen Label
        'view_appt_find_btn': 'சந்திப்பைக் கண்டுபிடி', # New Screen Button
        'view_appt_not_found': '"{name}"க்கான சந்திப்பு எதுவும் இல்லை.', # New Screen Message
        # Updated to show more details from DB
        'view_appt_found': '{name}க்கான சந்திப்பு:\nவயது: {age}\nதொலைபேசி: {phone}\nஇரத்த வகை: {blood}\nமருத்துவர்: {doctor}',
    }
}

# Map display names to language keys
LANGUAGE_MAP = {
    'English': 'en',
    'हिंदी (Hindi)': 'hi',
    'தமிழ் (Tamil)': 'ta'
}
# Reverse map for setting the combobox
DISPLAY_MAP = {v: k for k, v in LANGUAGE_MAP.items()}


# ---------------- COLORS AND FONTS ----------------
BG_COLOR = "#f7f0ff"
PURPLE = "#7a42f4"
PURPLE_ACTIVE = "#5a22c4" # Darker purple for button press
GREY = "#f0f0f0"
GREY_ACTIVE = "#e0e0e0"
GREY_TEXT = "#333333"

# --- Add Tamil/Hindi Fonts ---
# Use Nirmala UI as it supports many Indian scripts
FONT_BOLD = ("Segoe UI", 14, "bold")
FONT_NORMAL = ("Segoe UI", 11)
FONT_SEARCH = ("Segoe UI", 16, "bold")
FONT_BTN_LARGE = ("Nirmala UI", 13, "bold") # Use Nirmala for buttons
FONT_BTN_SMALL = ("Nirmala UI", 12, "bold")
FONT_LABEL = ("Nirmala UI", 12, "bold")
FONT_ENTRY = ("Segoe UI", 12)
FONT_TAMIL_HINDI = ("Nirmala UI", 10) # Specific font for disclaimer text


# Handle Pillow/PIL version differences for resizing
try:
    LANCZOS_RESAMPLE = Image.Resampling.LANCZOS
except AttributeError:
    # Fallback for older PIL versions
    LANCZOS_RESAMPLE = Image.LANCZOS

# ---------------- DATABASE CONNECTION ----------------
def create_db_connection():
    """Establishes a connection to the MySQL database."""
    connection = None
    try:
        # --- IMPORTANT: Replace with your actual credentials ---
        connection = mysql.connector.connect(
            host="localhost",       # Or your MySQL server address
            user="root",            # Your MySQL username
            password="SuryaPro@123",          # Your MySQL password (leave empty if none)
            database="yshy_app_db"    # The database name you created
        )
        # print("MySQL Database connection successful") # Uncomment for debugging
    except Error as e:
        # Display connection errors in a messagebox
        lang_key = app.current_lang_key.get() if 'app' in globals() else 'en'
        messagebox.showerror("Database Error", LANGUAGES[lang_key]['db_connection_error'].format(e=e))
        print(f"Error connecting to MySQL Database: {e}") # Keep console log too
    return connection

# ---------------- CUSTOM WIDGETS ----------------

class RoundedButton(tk.Frame):
    """A custom rounded button made with a Canvas."""
    def __init__(self, parent, width, height, radius, text,
                 bg, fg, active_bg, active_fg, font, command, text_key=None):
        
        super().__init__(parent, bg=parent.cget("bg"))
        self.width = width
        self.height = height
        self.radius = radius
        self.text = text
        self.text_key = text_key # --- i18n ---
        self.font = font
        self.bg = bg
        self.fg = fg
        self.active_bg = active_bg
        self.active_fg = active_fg
        self.command = command
        
        self.canvas = tk.Canvas(self, width=width, height=height, bg=parent.cget("bg"),
                                borderwidth=0, highlightthickness=0)
        self.canvas.pack()
        
        # Store text_id to update it later
        self.text_id = self.canvas.create_text(width/2, height/2, text=self.text, fill=self.fg, font=self.font)
        self.draw_button(self.bg, self.fg, initial=True) # Draw initial state
        
        # Bind mouse events
        self.canvas.bind("<Button-1>", self.on_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Enter>", self.on_enter)
        self.canvas.bind("<Leave>", self.on_leave)
    
    def pack(self, *args, **kwargs):
        super().pack(*args, **kwargs)

    def place(self, *args, **kwargs):
        super().place(*args, **kwargs)

    def draw_button(self, btn_bg, text_fg, initial=False):
        self.canvas.delete("all")
        
        r = self.radius
        w = self.width
        h = self.height
        
        self.canvas.create_oval(0, 0, 2*r, 2*r, fill=btn_bg, outline=btn_bg)
        self.canvas.create_oval(w-2*r, 0, w, 2*r, fill=btn_bg, outline=btn_bg)
        self.canvas.create_oval(0, h-2*r, 2*r, h, fill=btn_bg, outline=btn_bg)
        self.canvas.create_oval(w-2*r, h-2*r, w, h, fill=btn_bg, outline=btn_bg)
        self.canvas.create_rectangle(r, 0, w-r, h, fill=btn_bg, outline=btn_bg)
        self.canvas.create_rectangle(0, r, w, h-r, fill=btn_bg, outline=btn_bg)
        
        self.text_id = self.canvas.create_text(w/2, h/2, text=self.text, fill=text_fg, font=self.font)

    # --- i18n: New method to update text ---
    def update_text(self, new_text):
        self.text = new_text
        self.canvas.itemconfig(self.text_id, text=new_text)
    # --- End i18n ---

    def on_press(self, event):
        self.draw_button(self.active_bg, self.active_fg)

    def on_release(self, event):
        self.draw_button(self.bg, self.fg)
        if self.command:
            self.command()

    def on_enter(self, event):
        pass

    def on_leave(self, event):
        self.draw_button(self.bg, self.fg)


class ScrollableFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(bg=parent.cget("bg"))
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, bg=parent.cget("bg"))
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=parent.cget("bg"))
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.bind_all_mousewheel()
        
    def on_frame_configure(self, event):
        self.update_scroll_region()

    def update_scroll_region(self):
        self.canvas.update_idletasks()
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def on_mousewheel(self, event):
        if event.num == 4: delta = -1
        elif event.num == 5: delta = 1
        else: delta = -int(event.delta / 120)
        self.canvas.yview_scroll(delta, "units")

    def bind_all_mousewheel(self):
        self.bind_all("<MouseWheel>", self.on_mousewheel, add=True)
        self.bind_all("<Button-4>", self.on_mousewheel, add=True)
        self.bind_all("<Button-5>", self.on_mousewheel, add=True)

    def unbind_all_mousewheel(self):
        self.unbind_all("<MouseWheel>")
        self.unbind_all("<Button-4>")
        self.unbind_all("<Button-5>")

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.bind_all_mousewheel()
        self.canvas.yview_moveto(0.0)
    
    def lower(self, *args, **kwargs):
        super().lower(*args, **kwargs)
        self.unbind_all_mousewheel()


# --------------- MAIN APP CLASS -------------------
class YshyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(LANGUAGES['en']['app_title']) # Set initial title
        self.geometry("420x720")
        self.config(bg=BG_COLOR)
        self.resizable(False, False)
        
        self.frame_history = []
        self.current_image_path = None
        self.temp_image_name = "temp_capture.png" # For camera

        # --- i18n: Language State ---
        self.current_lang_name = tk.StringVar(value='English')
        self.current_lang_key = tk.StringVar(value='en')
        self.current_lang_name.trace_add('write', self.on_language_change)
        # --- End i18n ---

        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        
        self.style.configure('Custom.TCombobox',
                             font=FONT_ENTRY,
                             fieldbackground='white',
                             background='white',
                             foreground='black',
                             arrowcolor=PURPLE,
                             bordercolor=GREY,
                             lightcolor=GREY,
                             darkcolor=GREY,
                             padding=5)
        self.style.map('Custom.TCombobox',
                       fieldbackground=[('readonly', 'white')],
                       selectbackground=[('readonly', 'white')],
                       selectforeground=[('readonly', 'black')])
                       
        self.style.configure('Vertical.TScrollbar',
                             gripcount=0, background=GREY_ACTIVE,
                             darkcolor=GREY, lightcolor=GREY,
                             troughcolor=GREY, bordercolor=GREY,
                             arrowsize=16, arrowcolor=PURPLE)
        self.style.map('Vertical.TScrollbar',
                       background=[('active', PURPLE_ACTIVE), ('!active', GREY_ACTIVE)])

        self.container = tk.Frame(self, bg=BG_COLOR)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        # --- ADDED DermatologistScreen AND ViewAppointmentScreen ---
        for F in (HomeScreen, SearchScreen, DisclaimerScreen, AppointmentScreen, ScanResultScreen, DermatologistScreen, ViewAppointmentScreen):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame(HomeScreen)

    # --- i18n: Language change handler ---
    def on_language_change(self, *args):
        lang_name = self.current_lang_name.get()
        lang_key = LANGUAGE_MAP.get(lang_name, 'en')
        self.current_lang_key.set(lang_key)
        
        # Update title
        self.title(LANGUAGES[lang_key]['app_title'])

        # Tell all frames to update their text
        for frame in self.frames.values():
            if hasattr(frame, 'update_text'):
                frame.update_text(lang_key)
    # --- End i18n ---

    def show_frame(self, page_class):
        if self.frame_history and page_class == self.frame_history[-1]:
            return
        self.frame_history.append(page_class)
        frame = self.frames[page_class]
        frame.tkraise()

    def go_back(self):
        if len(self.frame_history) > 1:
            self.frame_history.pop()
            prev_page_class = self.frame_history[-1]
            frame = self.frames[prev_page_class]
            frame.tkraise()
            
    # --- Destructor to clean up temp image ---
    def __del__(self):
        # Attempt to remove temp image file if it exists
        try:
            if os.path.exists(self.temp_image_name):
                os.remove(self.temp_image_name)
        except Exception as e:
            print(f"Could not remove temp file {self.temp_image_name}: {e}")



# ---------------- HOME SCREEN ----------------
class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller

        self.title_label = tk.Label(self, text="Yshy", bg=BG_COLOR, fg="black", font=("Segoe UI", 22, "bold"))
        self.title_label.pack(pady=25)

        self.search_btn = RoundedButton(
            self, width=340, height=60, radius=30,
            text=LANGUAGES['en']['search_btn'], text_key='search_btn',
            bg=GREY, fg=GREY_TEXT, active_bg=GREY_ACTIVE, active_fg=GREY_TEXT, # --- MODIFIED: Made search button greyer ---
            font=FONT_SEARCH,
            command=lambda: controller.show_frame(SearchScreen)
        )
        self.search_btn.pack(pady=(15, 10)) # Reduced padding

        # --- i18n: Language Dropdown ---
        self.lang_menu = ttk.Combobox(
            self,
            textvariable=controller.current_lang_name,
            values=list(LANGUAGE_MAP.keys()),
            style='Custom.TCombobox',
            font=("Nirmala UI", 11),
            state="readonly",
            width=15
        )
        self.lang_menu.pack(pady=(0, 10))
        # --- End i18n ---

        def open_file():
            file_path = filedialog.askopenfilename(
                title="Choose an image",
                filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")]
            )
            if file_path:
                controller.current_image_path = file_path
                controller.show_frame(ScanResultScreen)

        def take_photo():
            # --- CAMERA FEATURE ---
            # We will implement the full logic in Phase 2
            # For now, show a message.
            lang_key = controller.current_lang_key.get()
            messagebox.showinfo("Camera", "Camera feature coming soon!\nकैमरा सुविधा जल्द ही आ रही है!\nகேமரா அம்சம் விரைவில்!")
            
            # --- Placeholder logic to proceed ---
            # controller.current_image_path = None
            # controller.show_frame(ScanResultScreen)


        btn_width = 340
        btn_height = 55
        btn_radius = 20
        # --- FIX: Adjusted padding ---
        btn_pady = 10 # Reset padding between buttons

        self.photo_btn = RoundedButton(
            self, width=btn_width, height=btn_height, radius=btn_radius,
            text=LANGUAGES['en']['take_photo_btn'], text_key='take_photo_btn',
            bg=PURPLE, fg="white", active_bg=PURPLE_ACTIVE, active_fg="white",
            font=FONT_BTN_LARGE,
            command=take_photo
        )
        self.photo_btn.pack(pady=btn_pady)
        
        self.gallery_btn = RoundedButton(
            self, width=btn_width, height=btn_height, radius=btn_radius,
            text=LANGUAGES['en']['gallery_btn'], text_key='gallery_btn',
            bg=PURPLE, fg="white", active_bg=PURPLE_ACTIVE, active_fg="white",
            font=FONT_BTN_LARGE,
            command=open_file
        )
        self.gallery_btn.pack(pady=btn_pady)

        # --- REMOVED View Appointment Button ---

        self.privacy_btn = RoundedButton(
            self, width=btn_width, height=btn_height, radius=btn_radius,
            text=LANGUAGES['en']['privacy_btn'], text_key='privacy_btn',
            bg=PURPLE, fg="white", active_bg=PURPLE_ACTIVE, active_fg="white",
            font=FONT_BTN_LARGE,
            command=lambda: controller.show_frame(DisclaimerScreen)
        )
        self.privacy_btn.pack(pady=btn_pady)
        
        self.update_text(controller.current_lang_key.get()) # Set initial text

    # --- i18n: Update text method ---
    def update_text(self, lang_key):
        self.title_label.config(text=LANGUAGES[lang_key]['app_title'])
        self.search_btn.update_text(LANGUAGES[lang_key]['search_btn'])
        self.photo_btn.update_text(LANGUAGES[lang_key]['take_photo_btn'])
        self.gallery_btn.update_text(LANGUAGES[lang_key]['gallery_btn'])
        # self.view_appt_btn removed
        self.privacy_btn.update_text(LANGUAGES[lang_key]['privacy_btn'])
        # Set combobox value from key
        self.controller.current_lang_name.set(DISPLAY_MAP[lang_key])
    # --- End i18n ---


# ---------------- SEARCH SCREEN ----------------
# (Moved View Appointment button here)
class SearchScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        
        top_frame = tk.Frame(self, bg=BG_COLOR)
        top_frame.pack(side="top", fill="x", pady=10, padx=10)

        self.back_btn = RoundedButton(
            top_frame, width=80, height=35, radius=15,
            text=LANGUAGES['en']['back_btn'], text_key='back_btn',
            bg=BG_COLOR, fg=PURPLE, active_bg=GREY, active_fg=PURPLE_ACTIVE,
            font=("Segoe UI", 11, "bold"),
            command=lambda: controller.go_back()
        )
        self.back_btn.pack(side="left")

        center_frame = tk.Frame(self, bg=BG_COLOR)
        center_frame.pack(fill="both", expand=True)
        button_wrapper = tk.Frame(center_frame, bg=BG_COLOR)
        button_wrapper.pack(expand=True)

        btn_width = 340
        btn_height = 55
        btn_radius = 20
        # --- Adjusted padding ---
        btn_pady = 12

        self.appointment_btn = RoundedButton(
            button_wrapper, width=btn_width, height=btn_height, radius=btn_radius,
            text=LANGUAGES['en']['create_appointment_btn'], text_key='create_appointment_btn',
            bg=PURPLE, fg="white", active_bg=PURPLE_ACTIVE, active_fg="white",
            font=FONT_BTN_LARGE,
            command=lambda: controller.show_frame(AppointmentScreen)
        )
        self.appointment_btn.pack(pady=btn_pady)

        self.dermatologist_btn = RoundedButton(
            button_wrapper, width=btn_width, height=btn_height, radius=btn_radius,
            text=LANGUAGES['en']['find_dermatologist_btn'], text_key='find_dermatologist_btn',
            bg=PURPLE, fg="white", active_bg=PURPLE_ACTIVE, active_fg="white",
            font=FONT_BTN_LARGE,
            command=lambda: controller.show_frame(DermatologistScreen)
        )
        self.dermatologist_btn.pack(pady=btn_pady)

        # --- ADDED View Appointment Button Here ---
        self.view_appt_btn = RoundedButton(
            button_wrapper, width=btn_width, height=btn_height, radius=btn_radius,
            text=LANGUAGES['en']['view_appointment_btn'], text_key='view_appointment_btn',
            bg=PURPLE, fg="white", active_bg=PURPLE_ACTIVE, active_fg="white",
            font=FONT_BTN_LARGE,
            command=lambda: controller.show_frame(ViewAppointmentScreen)
        )
        self.view_appt_btn.pack(pady=btn_pady)
        # --- END ADDED Button ---
        
    def update_text(self, lang_key):
        self.back_btn.update_text(LANGUAGES[lang_key]['back_btn'])
        self.appointment_btn.update_text(LANGUAGES[lang_key]['create_appointment_btn'])
        self.dermatologist_btn.update_text(LANGUAGES[lang_key]['find_dermatologist_btn'])
        self.view_appt_btn.update_text(LANGUAGES[lang_key]['view_appointment_btn']) # Update new button text


# ---------------- SCAN RESULT SCREEN ----------------
# (No changes needed here)
class ScanResultScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        self.image_tk = None

        top_frame = tk.Frame(self, bg=BG_COLOR)
        top_frame.pack(side="top", fill="x", pady=10, padx=10)

        self.back_btn = RoundedButton(
            top_frame, width=80, height=35, radius=15,
            text=LANGUAGES['en']['back_btn'], text_key='back_btn',
            bg=BG_COLOR, fg=PURPLE, active_bg=GREY, active_fg=PURPLE_ACTIVE,
            font=("Segoe UI", 11, "bold"),
            command=lambda: controller.go_back()
        )
        self.back_btn.pack(side="left")

        self.scroll_frame = ScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True)
        content = self.scroll_frame.scrollable_frame

        self.scan_title_label = tk.Label(content, text=LANGUAGES['en']['scan_title'], bg=BG_COLOR, fg="black", font=("Nirmala UI", 16, "bold"))
        self.scan_title_label.pack(pady=(10, 10))
        self.scan_confidence_label = tk.Label(content, text=LANGUAGES['en']['scan_confidence'], bg=BG_COLOR, fg="gray", font=("Segoe UI", 12))
        self.scan_confidence_label.pack(pady=5)

        self.image_canvas = tk.Canvas(content, width=300, height=180, bg="#d9c6ff", highlightthickness=0)
        self.image_canvas_text = self.image_canvas.create_text(150, 90, text=LANGUAGES['en']['scan_image_placeholder'], fill="black", font=("Segoe UI", 12))
        self.image_canvas.pack(pady=10)

        self.scan_disclaimer_label = tk.Label(
            content, text=LANGUAGES['en']['scan_disclaimer'], bg=BG_COLOR,
            wraplength=350, justify="center", fg="black", font=FONT_TAMIL_HINDI
        )
        self.scan_disclaimer_label.pack(pady=5)

        self.treatment_title_label = tk.Label(content, text=LANGUAGES['en']['scan_treatment_title'], bg=BG_COLOR, fg="black", font=FONT_BOLD)
        self.treatment_body_label = tk.Label(content, text=LANGUAGES['en']['scan_treatment_body'], bg=BG_COLOR, fg="black", justify="left", font=FONT_NORMAL, wraplength=340)
        self.section(self.treatment_title_label, self.treatment_body_label)

        self.food_title_label = tk.Label(content, text=LANGUAGES['en']['scan_food_title'], bg=BG_COLOR, fg="black", font=FONT_BOLD)
        self.food_body_label = tk.Label(content, text=LANGUAGES['en']['scan_food_body'], bg=BG_COLOR, fg="black", justify="left", font=FONT_NORMAL, wraplength=340)
        self.section(self.food_title_label, self.food_body_label)

        self.otc_title_label = tk.Label(content, text=LANGUAGES['en']['scan_otc_title'], bg=BG_COLOR, fg="black", font=FONT_BOLD)
        self.otc_body_label = tk.Label(content, text=LANGUAGES['en']['scan_otc_body'], bg=BG_COLOR, fg="black", justify="left", font=FONT_NORMAL, wraplength=340)
        self.section(self.otc_title_label, self.otc_body_label)
        
        btn_frame = tk.Frame(content, bg=BG_COLOR)
        btn_frame.pack(pady=25)
        
        btn_width = 340
        btn_height = 55
        btn_radius = 20

        self.appointment_btn = RoundedButton(
            btn_frame, width=btn_width, height=btn_height, radius=btn_radius,
            text=LANGUAGES['en']['create_appointment_btn'], text_key='create_appointment_btn',
            bg=PURPLE, fg="white", active_bg=PURPLE_ACTIVE, active_fg="white",
            font=FONT_BTN_LARGE,
            command=lambda: controller.show_frame(AppointmentScreen)
        )
        self.appointment_btn.pack(pady=15)

        self.dermatologist_btn = RoundedButton(
            btn_frame, width=btn_width, height=btn_height, radius=btn_radius,
            text=LANGUAGES['en']['find_dermatologist_btn'], text_key='find_dermatologist_btn',
            bg=PURPLE, fg="white", active_bg=PURPLE_ACTIVE, active_fg="white",
            font=FONT_BTN_LARGE,
            command=lambda: controller.show_frame(DermatologistScreen)
        )
        self.dermatologist_btn.pack(pady=15)
        
        tk.Frame(content, height=20, bg=BG_COLOR).pack()

    def section(self, title_label, body_label):
        title_label.pack(anchor="w", padx=20, pady=5)
        body_label.pack(anchor="w", padx=35)

    def load_image(self):
        file_path = self.controller.current_image_path
        lang_key = self.controller.current_lang_key.get()
        self.image_canvas.delete("all")
        
        if file_path:
            try:
                image = Image.open(file_path)
                image.thumbnail((300, 180), LANCZOS_RESAMPLE)
                self.image_tk = ImageTk.PhotoImage(image)
                self.image_canvas.create_image(150, 90, anchor="center", image=self.image_tk)
            except Exception as e:
                print(f"Error loading image: {e}")
                self.image_canvas_text = self.image_canvas.create_text(150, 90, text=LANGUAGES[lang_key]['scan_image_error'], fill="red", font=("Segoe UI", 12))
        else:
             # Need to recreate the text item if it was deleted
             self.image_canvas_text = self.image_canvas.create_text(150, 90, text=LANGUAGES[lang_key]['scan_image_placeholder'], fill="black", font=("Segoe UI", 12))


    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.update_text(self.controller.current_lang_key.get()) # Update text first
        self.load_image() # Then load image
        self.controller.update_idletasks()
        self.scroll_frame.update_scroll_region()

    def update_text(self, lang_key):
        self.back_btn.update_text(LANGUAGES[lang_key]['back_btn'])
        self.scan_title_label.config(text=LANGUAGES[lang_key]['scan_title'])
        self.scan_confidence_label.config(text=LANGUAGES[lang_key]['scan_confidence'])
        self.scan_disclaimer_label.config(text=LANGUAGES[lang_key]['scan_disclaimer'])
        
        # Update canvas text placeholder (load_image handles actual image text logic)
        try:
            # Check if self.image_canvas_text exists and is valid
            if self.image_canvas.type(self.image_canvas_text) == 'text':
                 self.image_canvas.itemconfig(self.image_canvas_text, text=LANGUAGES[lang_key]['scan_image_placeholder'])
            else: # If not valid text item (maybe image shown), recreate text
                 self.image_canvas_text = self.image_canvas.create_text(150, 90, text=LANGUAGES[lang_key]['scan_image_placeholder'], fill="black", font=("Segoe UI", 12))
                 # Immediately hide it if an image should be there
                 if self.controller.current_image_path:
                     self.image_canvas.itemconfig(self.image_canvas_text, state='hidden')

        except tk.TclError: # If item doesn't exist at all
             self.image_canvas_text = self.image_canvas.create_text(150, 90, text=LANGUAGES[lang_key]['scan_image_placeholder'], fill="black", font=("Segoe UI", 12))
             if self.controller.current_image_path:
                 self.image_canvas.itemconfig(self.image_canvas_text, state='hidden')

        self.treatment_title_label.config(text=LANGUAGES[lang_key]['scan_treatment_title'])
        self.treatment_body_label.config(text=LANGUAGES[lang_key]['scan_treatment_body'])
        self.food_title_label.config(text=LANGUAGES[lang_key]['scan_food_title'])
        self.food_body_label.config(text=LANGUAGES[lang_key]['scan_food_body'])
        self.otc_title_label.config(text=LANGUAGES[lang_key]['scan_otc_title'])
        self.otc_body_label.config(text=LANGUAGES[lang_key]['scan_otc_body'])
        
        self.appointment_btn.update_text(LANGUAGES[lang_key]['create_appointment_btn'])
        self.dermatologist_btn.update_text(LANGUAGES[lang_key]['find_dermatologist_btn'])


# ---------------- APPOINTMENT SCREEN ----------------
# (Modified submit_report for DB insert)
class AppointmentScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        
        self.controller = controller
        # self.report_data removed, no longer needed

        top_frame = tk.Frame(self, bg=BG_COLOR)
        top_frame.pack(side="top", fill="x", pady=10, padx=10)

        self.back_btn = RoundedButton(
            top_frame, width=80, height=35, radius=15,
            text=LANGUAGES['en']['back_btn'], text_key='back_btn',
            bg=BG_COLOR, fg=PURPLE, active_bg=GREY, active_fg=PURPLE_ACTIVE,
            font=("Segoe UI", 11, "bold"),
            command=lambda: [controller.go_back(), self.reset_form()]
        )
        self.back_btn.pack(side="left")

        self.title_label = tk.Label(self, text=LANGUAGES['en']['appointment_title'], bg=BG_COLOR, fg="black", font=("Nirmala UI", 18, "bold"))
        self.title_label.pack(pady=(10, 20))

        form_frame = tk.Frame(self, bg=BG_COLOR)
        form_frame.pack(pady=10, padx=40)

        entry_width = 25
        entry_font = FONT_ENTRY
        label_font = FONT_LABEL

        self.name_label = tk.Label(form_frame, text=LANGUAGES['en']['form_name'], font=label_font, bg=BG_COLOR)
        self.name_label.grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = tk.Entry(form_frame, width=entry_width, font=entry_font, relief="flat")
        self.name_entry.grid(row=0, column=1, pady=5, ipady=4)

        self.age_label = tk.Label(form_frame, text=LANGUAGES['en']['form_age'], font=label_font, bg=BG_COLOR)
        self.age_label.grid(row=1, column=0, sticky="w", pady=5)
        self.age_entry = tk.Entry(form_frame, width=entry_width, font=entry_font, relief="flat")
        self.age_entry.grid(row=1, column=1, pady=5, ipady=4)

        self.phone_label = tk.Label(form_frame, text=LANGUAGES['en']['form_phone'], font=label_font, bg=BG_COLOR)
        self.phone_label.grid(row=2, column=0, sticky="w", pady=5)
        self.phone_entry = tk.Entry(form_frame, width=entry_width, font=entry_font, relief="flat")
        self.phone_entry.grid(row=2, column=1, pady=5, ipady=4)

        self.blood_label = tk.Label(form_frame, text=LANGUAGES['en']['form_blood'], font=label_font, bg=BG_COLOR)
        self.blood_label.grid(row=3, column=0, sticky="w", pady=5)
        self.blood_group_var = tk.StringVar()
        blood_groups = ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"]
        self.blood_group_menu = ttk.Combobox(form_frame, textvariable=self.blood_group_var,
                                             values=blood_groups, width=entry_width-2,
                                             font=entry_font, style='Custom.TCombobox',
                                             state="readonly")
        self.blood_group_menu.grid(row=3, column=1, pady=5, ipady=1)

        self.doctor_label = tk.Label(form_frame, text=LANGUAGES['en']['form_doctor'], font=label_font, bg=BG_COLOR)
        self.doctor_label.grid(row=4, column=0, sticky="w", pady=5)
        self.doctor_var = tk.StringVar()
        self.doctors = ["Dr Tiwari", "Dr Goyal"] # Store for i18n
        self.doctor_menu = ttk.Combobox(form_frame, textvariable=self.doctor_var,
                                        values=self.doctors, width=entry_width-2,
                                        font=entry_font, style='Custom.TCombobox',
                                        state="readonly")
        self.doctor_menu.grid(row=4, column=1, pady=5, ipady=1)

        self.success_label = tk.Label(self, text=LANGUAGES['en']['form_success_msg'], bg=BG_COLOR, fg="green", font=("Segoe UI", 12, "bold"))
        
        self.submit_btn = RoundedButton(
            self, width=300, height=50, radius=20,
            text=LANGUAGES['en']['form_submit_btn'], text_key='form_submit_btn',
            bg=PURPLE, fg="white", active_bg=PURPLE_ACTIVE, active_fg="white",
            font=FONT_BTN_LARGE,
            command=self.submit_report
        )
        self.submit_btn.pack(pady=20)

        # Print button removed as we save to DB now

    # --- MODIFIED: submit_report saves to MySQL ---
    def submit_report(self):
        lang_key = self.controller.current_lang_key.get()
        name = self.name_entry.get().strip()
        age_str = self.age_entry.get().strip()
        phone = self.phone_entry.get().strip()
        blood = self.blood_group_var.get()
        doc = self.doctor_var.get()

        # --- Validate Data ---
        if not all([name, age_str, phone, blood, doc]):
            messagebox.showerror("Error", LANGUAGES[lang_key]['form_err_all_fields'])
            return
        try:
            age = int(age_str) # Convert age to integer
        except ValueError:
            messagebox.showerror("Error", LANGUAGES[lang_key]['form_err_age_number'])
            return
        if not phone.isdigit() or len(phone) < 7:
            messagebox.showerror("Error", LANGUAGES[lang_key]['form_err_phone_invalid'])
            return

        # --- Database Interaction ---
        connection = create_db_connection()
        if connection is None:
            return # Error handled in create_db_connection

        cursor = connection.cursor()
        query = """
            INSERT INTO appointments (name, age, phone, blood_group, doctor)
            VALUES (%s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (name, age, phone, blood, doc))
            connection.commit()
            print("Appointment inserted successfully") # For debugging

            # --- Update UI ---
            self.submit_btn.pack_forget()       # Hide submit button
            self.success_label.pack(pady=15)     # Show success message
            messagebox.showinfo(LANGUAGES[lang_key]['form_success_title'], LANGUAGES[lang_key]['form_success_body'])

        except Error as e:
            print(f"Error inserting appointment: {e}")
            messagebox.showerror("Database Error", LANGUAGES[lang_key]['db_insert_error'].format(e=e))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                # print("MySQL connection is closed") # For debugging

    # Print report function removed

    def reset_form(self):
        """Resets the form to its initial state."""
        self.name_entry.delete(0, 'end')
        self.age_entry.delete(0, 'end')
        self.phone_entry.delete(0, 'end')
        self.blood_group_var.set("")
        self.doctor_var.set("")
        
        self.success_label.pack_forget()
        # self.print_btn removed
        self.submit_btn.pack(pady=20) # Ensure submit button is visible again
        # self.report_data removed

    def update_text(self, lang_key):
        self.back_btn.update_text(LANGUAGES[lang_key]['back_btn'])
        self.title_label.config(text=LANGUAGES[lang_key]['appointment_title'])
        self.name_label.config(text=LANGUAGES[lang_key]['form_name'])
        self.age_label.config(text=LANGUAGES[lang_key]['form_age'])
        self.phone_label.config(text=LANGUAGES[lang_key]['form_phone'])
        self.blood_label.config(text=LANGUAGES[lang_key]['form_blood'])
        self.doctor_label.config(text=LANGUAGES[lang_key]['form_doctor'])
        # Note: Doctor names and blood groups are not translated, which is standard.
        self.submit_btn.update_text(LANGUAGES[lang_key]['form_submit_btn'])
        # self.print_btn removed
        self.success_label.config(text=LANGUAGES[lang_key]['form_success_msg'])


# ---------------- DISCLAIMER SCREEN ----------------
# (No changes needed here)
class DisclaimerScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller

        top_frame = tk.Frame(self, bg=BG_COLOR)
        top_frame.pack(side="top", fill="x", pady=10, padx=10)

        self.back_btn = RoundedButton(
            top_frame, width=80, height=35, radius=15,
            text=LANGUAGES['en']['back_btn'], text_key='back_btn',
            bg=BG_COLOR, fg=PURPLE, active_bg=GREY, active_fg=PURPLE_ACTIVE,
            font=("Segoe UI", 11, "bold"),
            command=lambda: controller.go_back()
        )
        self.back_btn.pack(side="left")

        self.title_label = tk.Label(self, text=LANGUAGES['en']['disclaimer_title'], bg=BG_COLOR, fg="red", font=("Nirmala UI", 16, "bold"))
        self.title_label.pack(pady=(10, 15))

        self.scroll_frame = ScrollableFrame(self)
        self.scroll_frame.pack(padx=20, pady=5, fill="both", expand=True)
        content = self.scroll_frame.scrollable_frame

        self.text_label = tk.Label(content, text=LANGUAGES['en']['disclaimer_body'], bg=BG_COLOR, fg="black",
                                     font=FONT_TAMIL_HINDI, wraplength=340, justify="left")
        self.text_label.pack(fill="both", expand=True, padx=5)

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.controller.update_idletasks()
        self.scroll_frame.update_scroll_region()
        self.update_text(self.controller.current_lang_key.get()) # Update text on raise

    def update_text(self, lang_key):
        self.back_btn.update_text(LANGUAGES[lang_key]['back_btn'])
        self.title_label.config(text=LANGUAGES[lang_key]['disclaimer_title'])
        self.text_label.config(text=LANGUAGES[lang_key]['disclaimer_body'])
    
    
# ---------------- DERMATOLOGIST SCREEN ----------------
# (No changes needed here)
class DermatologistScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller

        top_frame = tk.Frame(self, bg=BG_COLOR)
        top_frame.pack(side="top", fill="x", pady=10, padx=10)

        self.back_btn = RoundedButton(
            top_frame, width=80, height=35, radius=15,
            text=LANGUAGES['en']['back_btn'], text_key='back_btn',
            bg=BG_COLOR, fg=PURPLE, active_bg=GREY, active_fg=PURPLE_ACTIVE,
            font=("Segoe UI", 11, "bold"),
            command=lambda: controller.go_back()
        )
        self.back_btn.pack(side="left")

        self.title_label = tk.Label(self, text=LANGUAGES['en']['dermo_title'], bg=BG_COLOR, fg="black", font=("Nirmala UI", 18, "bold"))
        self.title_label.pack(pady=(10, 20))

        # --- Search Bar ---
        search_frame = tk.Frame(self, bg=BG_COLOR)
        search_frame.pack(pady=10, padx=30)
        
        self.pincode_label = tk.Label(search_frame, text=LANGUAGES['en']['dermo_pincode_label'], font=FONT_LABEL, bg=BG_COLOR)
        self.pincode_label.pack(pady=(0, 5))
        
        self.pincode_entry = tk.Entry(search_frame, width=15, font=FONT_ENTRY, relief="flat")
        self.pincode_entry.pack(pady=5, ipady=4)
        
        self.search_btn = RoundedButton(
            search_frame, width=120, height=40, radius=15,
            text=LANGUAGES['en']['dermo_search_btn'], text_key='dermo_search_btn',
            bg=PURPLE, fg="white", active_bg=PURPLE_ACTIVE, active_fg="white",
            font=FONT_BTN_SMALL,
            command=self.find_clinics
        )
        self.search_btn.pack(pady=10)

        # --- Results Area ---
        self.scroll_frame = ScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.results_frame = self.scroll_frame.scrollable_frame
        
        self.results_title = tk.Label(self.results_frame, text="", bg=BG_COLOR, font=FONT_BOLD)
        self.results_title.pack(pady=5)
        

    def find_clinics(self):
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            if widget != self.results_title: # Don't destroy the title
                widget.destroy()
        
        lang_key = self.controller.current_lang_key.get()
        pincode = self.pincode_entry.get()
        
        # Validate pincode
        if not (pincode.isdigit() and len(pincode) == 6):
            self.results_title.config(text=LANGUAGES[lang_key]['dermo_err_pincode'], fg="red")
            return
            
        self.results_title.config(text=LANGUAGES[lang_key]['dermo_results_title'].format(pincode=pincode), fg="black")

        # --- FAKE MOCK DATA ---
        clinics = [
            {'key_name': 'dermo_clinic1_name', 'key_desc': 'dermo_clinic1_desc'},
            {'key_name': 'dermo_clinic2_name', 'key_desc': 'dermo_clinic2_desc'},
            {'key_name': 'dermo_clinic3_name', 'key_desc': 'dermo_clinic3_desc'},
            {'key_name': 'dermo_clinic4_name', 'key_desc': 'dermo_clinic4_desc'},
        ]
        
        for clinic in clinics:
            frame = tk.Frame(self.results_frame, bg=GREY, borderwidth=1, relief="solid")
            
            name = LANGUAGES[lang_key][clinic['key_name']]
            desc = LANGUAGES[lang_key][clinic['key_desc']]
            
            tk.Label(frame, text=name, font=FONT_LABEL, bg=GREY, justify="left").pack(anchor="w", padx=10, pady=(10, 0))
            tk.Label(frame, text=desc, font=FONT_NORMAL, bg=GREY, justify="left").pack(anchor="w", padx=10, pady=(0, 10))
            
            frame.pack(fill="x", pady=5, padx=10)
            
        self.scroll_frame.update_scroll_region() # IMPORTANT


    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.controller.update_idletasks()
        self.scroll_frame.update_scroll_region()
        self.update_text(self.controller.current_lang_key.get()) # Update text on raise

    def update_text(self, lang_key):
        self.back_btn.update_text(LANGUAGES[lang_key]['back_btn'])
        self.title_label.config(text=LANGUAGES[lang_key]['dermo_title'])
        self.pincode_label.config(text=LANGUAGES[lang_key]['dermo_pincode_label'])
        self.search_btn.update_text(LANGUAGES[lang_key]['dermo_search_btn'])
        
        # Clear results on language change
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        self.results_title = tk.Label(self.results_frame, text="", bg=BG_COLOR, font=FONT_BOLD)
        self.results_title.pack(pady=5)
        self.pincode_entry.delete(0, 'end')


# --- VIEW APPOINTMENT SCREEN ---
# (Modified find_appointment for DB query)
class ViewAppointmentScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller

        top_frame = tk.Frame(self, bg=BG_COLOR)
        top_frame.pack(side="top", fill="x", pady=10, padx=10)

        self.back_btn = RoundedButton(
            top_frame, width=80, height=35, radius=15,
            text=LANGUAGES['en']['back_btn'], text_key='back_btn',
            bg=BG_COLOR, fg=PURPLE, active_bg=GREY, active_fg=PURPLE_ACTIVE,
            font=("Segoe UI", 11, "bold"),
            command=lambda: controller.go_back()
        )
        self.back_btn.pack(side="left")

        self.title_label = tk.Label(self, text=LANGUAGES['en']['view_appt_title'], bg=BG_COLOR, fg="black", font=("Nirmala UI", 18, "bold"))
        self.title_label.pack(pady=(10, 20))

        # --- Input Section ---
        input_frame = tk.Frame(self, bg=BG_COLOR)
        input_frame.pack(pady=10, padx=30)

        self.name_label = tk.Label(input_frame, text=LANGUAGES['en']['view_appt_name_label'], font=FONT_LABEL, bg=BG_COLOR)
        self.name_label.pack(pady=5)

        self.name_entry = tk.Entry(input_frame, width=25, font=FONT_ENTRY, relief="flat")
        self.name_entry.pack(pady=5, ipady=4)

        self.find_btn = RoundedButton(
            input_frame, width=200, height=45, radius=15,
            text=LANGUAGES['en']['view_appt_find_btn'], text_key='view_appt_find_btn',
            bg=PURPLE, fg="white", active_bg=PURPLE_ACTIVE, active_fg="white",
            font=FONT_BTN_LARGE,
            command=self.find_appointment
        )
        self.find_btn.pack(pady=15)

        # --- Results Area ---
        self.results_label = tk.Label(self, text="", bg=BG_COLOR, font=FONT_NORMAL, justify="left", wraplength=350)
        self.results_label.pack(pady=10, padx=30, fill="x")

    # --- MODIFIED: find_appointment queries MySQL ---
    def find_appointment(self):
        lang_key = self.controller.current_lang_key.get()
        name_to_find = self.name_entry.get().strip()

        if not name_to_find:
            self.results_label.config(text=LANGUAGES[lang_key]['view_appt_name_label'], fg='red')
            return

        # --- Database Interaction ---
        connection = create_db_connection()
        if connection is None:
            return

        cursor = connection.cursor()
        # Find the most recent appointment for that name
        query = "SELECT age, phone, blood_group, doctor FROM appointments WHERE name = %s ORDER BY submission_time DESC LIMIT 1"

        try:
            cursor.execute(query, (name_to_find,))
            result = cursor.fetchone() # Get the first result

            if result:
                # result = (age, phone, blood_group, doctor)
                result_text = LANGUAGES[lang_key]['view_appt_found'].format(
                    name=name_to_find,
                    age=result[0],
                    phone=result[1],
                    blood=result[2],
                    doctor=result[3]
                )
                self.results_label.config(text=result_text, fg='black')
            else:
                result_text = LANGUAGES[lang_key]['view_appt_not_found'].format(name=name_to_find)
                self.results_label.config(text=result_text, fg='red')

        except Error as e:
            print(f"Error querying appointment: {e}")
            messagebox.showerror("Database Error", LANGUAGES[lang_key]['db_query_error'].format(e=e))
            self.results_label.config(text=LANGUAGES[lang_key]['db_query_error'].format(e="Error"), fg='red')
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.update_text(self.controller.current_lang_key.get()) # Update text on raise
        self.name_entry.delete(0, 'end') # Clear entry on raise
        self.results_label.config(text="") # Clear results on raise


    def update_text(self, lang_key):
        self.back_btn.update_text(LANGUAGES[lang_key]['back_btn'])
        self.title_label.config(text=LANGUAGES[lang_key]['view_appt_title'])
        self.name_label.config(text=LANGUAGES[lang_key]['view_appt_name_label'])
        self.find_btn.update_text(LANGUAGES[lang_key]['view_appt_find_btn'])
        # Clear results label text when language changes
        self.results_label.config(text="")


# ---------------- RUN APP ----------------
# --- Add app to global scope for error handling in create_db_connection ---
if __name__ == "__main__":
    app = YshyApp()
    app.mainloop()