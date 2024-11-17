import streamlit as st
import pandas as pd

st.title('Principal Component Analysis: An Intuition')

#Motivation:
st.header('Motivation')
st.write('Principal Component Analysis (PCA) is often used in data analysis to project information on a smaller dimension '
         'while the variance in the data is _mostly_ preserved.')
st.write('Given below is a dataset containing two columns 2Y and 5Y US treasury yield changes')
st.dataframe(pd.read_csv('src/products/data/yield_changes.csv'))
st.write('If we scatter plot them on a graph, Can we see a pattern emerging from the data?')
st.image('src/products/data/two_five_yield_changes.png')

st.write('We can observe from the above graph that the data points are highly correlated.')

st.image('src/products/data/eigen_vector.png')
st.write('From the above graph, it is clear that rather than choosing 2Y and 5Y as the two dimension to represent the'
         ' data, we can choose a new basis p1 and p2 (depicted above) such that the variation along p2 is comparatively'
         ' less compared to variation along p1.')
st.write('PCA is used to get the above axes along which we can explain majority of the variance. Follow the below derivation '
         'to understand how it works.')
st.subheader('Derivation:')
st.write('Let ${X_{mn}}$ be the dataset with ${m}$ rows and ${n}$ columns and let ${P_{nn}}$ be the new basis we are'
         ' trying to find. ')
st.latex(r'''X=
\begin{bmatrix}
    x_{11} & x_{12} & x_{13} & \dots  & x_{1n} \\
    x_{21} & x_{22} & x_{23} & \dots  & x_{2n} \\
    \vdots & \vdots & \vdots & \ddots & \vdots \\
    x_{m1} & x_{m2} & x_{m3} & \dots  & x_{mn}
\end{bmatrix}
 P=
\begin{bmatrix}
    p_{11} & p_{12} & p_{13} & \dots  & p_{1n} \\
    p_{21} & p_{22} & p_{23} & \dots  & p_{2n} \\
    \vdots & \vdots & \vdots & \ddots & \vdots \\
    p_{n1} & p_{n2} & p_{n3} & \dots  & p_{nn}
\end{bmatrix}
''')
st.write('For example, we can interpret ${X}$ as the changes in yield for n bonds. We are already aware that many of the'
         'financial instruments have a non-zero correlations and bonds are no exception. A 2-year treasury bond and a'
         '5-year treasury bond move in a somewhat co-ordinated fashion. If there was a jump in yield for the 2-year bond,'
         'there is a significant probability that there is going to be jump in 5-year bond yield as well.'
         'So, ${x_{ij}}$ denotes the yield change of ${j^{th}}$ bond on ${i^{th}}$ day.')

st.subheader('Data Cleaning')

st.write('The first step we can take in data-cleaning here is to make mean of the columns as zero. This will help us '
         'in one of the next steps while deriving the covariance of the projected dataset. So, each column (yield changes '
         'of a bond) will be made zero mean.')



st.write('One way to look at the dataset is to look at each bond as a dimension and each datapoint is a row in ${X}$. '
    'So, projecting a bond\'s yield changes on the new basis can be written as follows:')

st.latex('''
    X_{i} = \\alpha_{i1}P_{1} + \\alpha_{i2}P_{2} + \\dots + \\alpha_{in}P_{n}\\newline
        \\space\\newline
    \\alpha_{ij} = x_{i}^{T} . P_{j}\\newline
        \\space\\newline
    \\hat{X} = X . P
''')

st.write('${\hat{X}}$ is the new projected dataset.')

st.subheader('What are the properties of $\hat{X}$?')

st.write('We can derive the covariance matrix of $\hat{X}$ and check how it is related to covariance of ${X}$')
st.write('But, first of all, what is the covariance matrix of ${X}$?')
st.latex('''
    \\Sigma_{ij} = \\dfrac{1}{m} \\Sigma_{k=1}^{m}(X_{ki} - \\mu_{i})(X_{kj} - \\mu_{j})
''')
st.write('Since, ${\\mu=0}$ for all the columns, covariance equation simplifies further:')

st.latex('''
    \\Sigma_{ij} = \\dfrac{1}{m} \\Sigma_{k=1}^{m}X_{ki}X_{kj} \\newline
    or\\newline
    \\Sigma = \\dfrac{1}{m} X^{T} X
''')
st.write('What is the covariance of $\\hat{X}$?')
st.latex('''
    \\hat{\\Sigma} = \\dfrac{1}{m} \\hat{X}^{T} \\hat{X} = \\dfrac{1}{m} (XP)^{T} XP = \\dfrac{1}{m} P^{T}X^{T}XP\\newline
    \\space\\newline
    \\hat{\\Sigma} = P^{T}\\Sigma P
''')

st.write('Since, we would like to have the new basis ${P}$ to have 0 cross correlations, $\\hat{\\Sigma}$ needs to be a '
         'diagonal matrix. For a diagonal matrix, ${P}$ should be eigen vectors of $\\Sigma$. Also, Eigen values will '
         'be the variance along each of the new axis upto a factor.')

st.write('Using the new basis, we can project the dataset onto this new basis and calculate the variance along each axis')
st.latex('''
    \\hat{X_{i}} = XP_{i}\\newline
    \\space\\newline
    \\hat{\\sigma_{i}} = \\dfrac{1}{m}X_{i}^{T}X_{i} = \\dfrac{1}{m}P_{i}^{T}X^{T}XP_{i}\\newline
    ''')
st.write('Since ${P_{i}}$ is an eigen vector of ${\\Sigma}$,')

st.latex('''
    \\hat{\\sigma_{i}} = \\dfrac{1}{m}P_{i}^{T} \\lambda_{i}P_{i}
''')
st.write('Also, since eigen vectors are orthonormal,')

st.latex('''
    \\hat{\\sigma_{i}} = \\dfrac{1}{m}\\lambda_{i}
''')
st.write('From the above derivation, we can say that the eigen vectors with highest eigen values will carry the highest '
         'variance.')

st.subheader('Error Estimation:')
st.write('Let\'s say we got the eigen vectors and eigen values. Can we quantify the error if we only use top k axes since '
         'the rest of axis doesn\'t carry less variance?')

st.latex('''
X_{i} = \\Sigma_{j=1}^{n} \\alpha_{ij}P_{j}\\newline
\\space\\newline
\\hat{X_{i}} = \\Sigma_{j=1}^{k} \\alpha_{ij}P_{j}\\newline
\\space\\newline
error = \\Sigma_{i=1}^{m}(X_{i} - \\hat{X_{i}})^{T}(X_{i} - \\hat{X_{i}})= \\Sigma_{i=1}^{m}(\\Sigma_{j=1}^{k} \\alpha_{ij}P_{j})^{T}(\\Sigma_{j=1}^{k} \\alpha_{ij}P_{j})\\newline
''')
st.write('Multiplying the terms gives us cross terms such as $P_{i}.P{j}$ where ${i\\neq j}$. Such cross terms evaluate to '
         'zero since $P_{i}$ are eigen vectors (orthonormal). Keeping the non-zero terms gives the following:')
st.latex('''
error = \\Sigma_{i=1}^{m}\\Sigma_{j=k+1}^{n} \\alpha_{ij}^{2} P_{j}^{T}P{j} = \\Sigma_{i=1}^{m}\\Sigma_{j=k+1}^{n} \\alpha_{ij}^{2} 
''')

st.write('Expanding ${\\alpha_{ij}}$,')

st.latex('''
error = \\Sigma_{i=1}^{m}\\Sigma_{j=k+1}^{n} (X_{i}^{T}P_{j})^{T}(X_{i}^{T}P_{j}) = \\Sigma_{i=1}^{m}\\Sigma_{j=k+1}^{n} 
P_{j}^{T}X_{i}X_{i}^{T}P_{j}\\newline
\\space\\newline
error = \\Sigma_{j=k+1}^{n} P_{j}^{T} m \\Sigma P_{j} =
 \\Sigma_{j=k+1}^{n} P_{j}^{T}m\\lambda_{j}P_{j} =
 \\Sigma_{j=k+1}^{n} m \\lambda_{j}
''')
st.write('From the above derivation, we can say that the error is the sum of eigen values corresponding to the eigen vectors '
         'excluded during reconstruction. This should give the reader a proper reason why we choose eigen vectors with highest '
         'eigen values.')




