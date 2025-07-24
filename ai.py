import google.generativeai as genai

APIkey = "AIzaSyA99rXwMfKPSHArGV2WjaOvmhXiYAmBo5w"
genai.configure(api_key=APIkey)
model = genai.GenerativeModel('gemini-2.5-flash')

prompt = """If I give you a contract, can you summarize it?, If you can, I have a challenge for you. Can you tell me the deadline, money, parties, description? And refrain from using any other text such as 'Of course I can' or 'this might not be accurate'. Here is the contract: 
This Service Agreement is made on July 10, 2025, between OceanView Resorts (“Client”) and PixelWorx Media (“Contractor”).

PixelWorx Media agrees to provide video production services for OceanView Resorts’ upcoming advertising campaign. The services will include scripting, filming, editing, and delivering a final promotional video of 2–3 minutes.

The total fee for the project is ₹80,000. OceanView Resorts will pay 50% (₹40,000) upfront and the remaining 50% upon delivery of the final video.

All deliverables must be completed and delivered by August 1, 2025. PixelWorx Media retains the right to use the completed video for its portfolio and promotional purposes. All commercial rights to the final video are granted to OceanView Resorts.

This agreement is governed by the laws of Maharashtra, India.

Signed,
OceanView Resorts  
PixelWorx Media

"""
response = model.generate_content(prompt)
print(response.text)