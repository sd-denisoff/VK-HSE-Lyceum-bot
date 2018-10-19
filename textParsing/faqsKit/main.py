import faqsKit

faqs = faqsKit.faqs()

while True:
    s = input()
    print(faqs.get(s))
