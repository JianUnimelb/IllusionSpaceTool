import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Set page configuration
# page_icon = Image.open("icon.png")
st.set_page_config(layout="wide", page_title="Illusion space")

# Header

st.header("Illusion Spaces in VR", divider='rainbow')

# Placeholder for abstract
abstract = "Explore the space of physical and virtual illusions in VR!"
st.markdown(abstract)

#########################################
st.subheader('Inputs', divider='rainbow')
st.write("Instructions 1: Input the parameters of your physical object from the sliders below, and its illusion space will be plotted for your reference")

# Sliders for input
physicalsize = st.slider("What is the Physical Size (cm)?", 3, 9, 6)
# st.write("Selected Size: ", physical_size)

physicalangle = st.slider("What is the Physical Taper Angle (°)?", 0, 16, 8)
# st.write("Selected Angle: ", physical_angle)
if physicalangle == 0:
    physicalangle = 0.1
# Drawing a shape with Matplotlib
fig, ax = plt.subplots(figsize=(5, 5))
av = np.linspace(-5, 5, 500)
SDT = (-0.010*physicalangle*av+0.005*physicalangle-0.002*av*physicalsize+0.087*av+0.001*physicalsize*physicalsize+0.035*physicalsize+0.275)/(-0.007*physicalangle+0.037*physicalsize+0.489)
SUT = (-0.004*physicalangle*av+0.001*physicalangle*physicalsize-0.030*physicalangle+0.009*av*physicalsize-0.093*av+0.001*physicalsize*physicalsize-0.086*physicalsize+1.778)/(-0.026*physicalangle-0.029*physicalsize+1.197)

plt.plot(av, SUT, label='Size upscaling thresholds', color = 'orange', linestyle='-', linewidth=2)
plt.plot(av, SDT, label='Size downscaling thresholds', color = 'violet', linestyle='-', linewidth=2)

sv = np.linspace(-5, 5, 500)
ADT = (0.001*physicalangle*physicalsize-0.011*physicalangle-0.001*physicalsize*physicalsize-0.008*physicalsize*sv-0.010*physicalsize+0.165*sv+0.275)/(-0.001*physicalangle-0.059*physicalsize+0.785)
AUT = (0.001*physicalangle*physicalsize-0.020*physicalangle*sv+0.010*physicalangle-0.001*physicalsize*physicalsize-0.074*physicalsize*sv+0.023*physicalsize+0.873*sv-0.054)/(0.005*physicalangle-0.047*physicalsize+0.604)
plt.plot(AUT, sv, label='Angle upscaling thresholds', color = 'lime', linestyle='--', linewidth=2)
plt.plot(ADT, sv, label='Angle downscaling thresholds', color = 'lightblue', linestyle='--', linewidth=2)

ax.set_xlim(0.2, 1.8)
ax.set_ylim(0.2, 1.8)
ax.set_xlabel("Virtual angle/physical angle")
ax.set_ylabel("Virtual size/physical size")
plt.legend(fontsize=12)
ax.set_aspect('equal')
ax.set_title('Illusion space for the physical object')
ax.grid(True)

# Display the Matplotlib figure in Streamlit
st.pyplot(fig)

st.write("Instructions 2: Please input the virtual angles for calculating (because it's influencing the size thresholds)")
virtualangle = st.slider("What is the Virtual Angle (°)?", 0,22,8)/physicalangle
sdt = (-0.010*physicalangle*virtualangle+0.005*physicalangle-0.002*virtualangle*physicalsize+0.087*virtualangle+0.001*physicalsize*physicalsize+0.035*physicalsize+0.275)/(-0.007*physicalangle+0.037*physicalsize+0.489)
sut = (-0.004*physicalangle*virtualangle+0.001*physicalangle*physicalsize-0.030*physicalangle+0.009*virtualangle*physicalsize-0.093*virtualangle+0.001*physicalsize*physicalsize-0.086*physicalsize+1.778)/(-0.026*physicalangle-0.029*physicalsize+1.197)

st.write("Virtual size should be larger than: ", sdt*physicalsize, "cm")
st.write("Virtual size should be smaller than: ", sut*physicalsize, "cm")
# st.write("Instructions 3: However, the virtual angle you input maybe outside the illusion spaces. After selecting the virtual size you need from the calculation above, please input it below to check if your virtual angle is within the illusion spaces.")

st.write("Instructions 3: Please input the virtual sizes for calculating (because it's influencing the angle thresholds)")
virtualsize = st.slider("What is the Virtual Size (cm)?", 1,11,6)/physicalsize
adt = (0.001*physicalangle*physicalsize-0.011*physicalangle-0.001*physicalsize*physicalsize-0.008*physicalsize*virtualsize-0.010*physicalsize+0.165*virtualsize+0.275)/(-0.001*physicalangle-0.059*physicalsize+0.785)
aut = (0.001*physicalangle*physicalsize-0.020*physicalangle*virtualsize+0.010*physicalangle-0.001*physicalsize*physicalsize-0.074*physicalsize*virtualsize+0.023*physicalsize+0.873*virtualsize-0.054)/(0.005*physicalangle-0.047*physicalsize+0.604)

st.write("Virtual angle should be larger than: ", adt*physicalangle, "°")
st.write("Virtual angle should be smaller than: ", aut*physicalangle, "°")

swithin = False
awithin = False
if sdt<virtualsize and sut>virtualsize:
    swithin = True
if adt<virtualangle and aut>virtualangle:
    awithin = True

if swithin == True and awithin == True:
    st.write('<p style="color:green;">Great! Your virtual properties are within the illusion spaces and the user will not notice the difference.</p>', unsafe_allow_html=True)
else:
    st.write('<p style="color:red;">Warning! Your virtual properties are outside the illusion spaces and the user will notice the difference.</p>', unsafe_allow_html=True)
    st.write(f'<p style="color:red;">The virtual size should be within {sdt*physicalsize}cm and {sut*physicalsize}cm.</p>', unsafe_allow_html=True)
    st.write(f'<p style="color:red;">The virtual angle should be within {adt*physicalangle}° and {aut*physicalangle}°.</p>', unsafe_allow_html=True)
