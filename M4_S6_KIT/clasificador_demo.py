import re, random
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import train_test_split

random.seed(7)
prods=["camarón","banano","cacao","flores","atún","petróleo","café"]
T={
"comercio exterior":["Las exportaciones de {p} sumaron {c} millones de USD en el período.","El valor exportado de {p} aumentó frente al mes anterior.","Las ventas externas de {p} se concentraron en pocos destinos.","Las importaciones de bienes de capital registraron {c} millones de USD.","La balanza comercial mostró un saldo distinto al del período previo.","El volumen embarcado de {p} fue menor al esperado."],
"precios":["El índice de precios al consumidor varió {c} puntos porcentuales.","El precio de la canasta básica subió en el mes.","La inflación mensual se ubicó por debajo del período anterior.","Los precios de los alimentos aumentaron en las principales ciudades.","La variación de precios de {p} fue la más alta de la canasta.","El costo de vida registró un incremento moderado."],
"empleo":["La tasa de desempleo se ubicó en {c} por ciento de la población activa.","El empleo adecuado aumentó respecto del trimestre anterior.","El subempleo se redujo en las zonas urbanas.","Las personas ocupadas en el sector de {p} sumaron {c} miles.","La población económicamente activa creció en el trimestre.","El empleo informal se mantuvo como la mayor parte de la ocupación."]}
cif=lambda: f"{random.randint(100,3999)},{random.randint(0,99):02d}"
rows=[(random.choice(ts).format(p=random.choice(prods),c=cif()),lab) for lab,ts in T.items() for _ in range(60)]
df=pd.DataFrame(rows,columns=["texto","tema"]).drop_duplicates().reset_index(drop=True)

def preprocess(t):
    t=t.lower()
    t=re.sub(r"\d+(?:[.,]\d+)*"," NUM ",t)
    return re.sub(r"\s+"," ",t).strip()
df["texto_limpio"]=df.texto.apply(preprocess)

# toy DTM
toy=["la tasa de empleo","el precio sube","empleo y precio"]
v=CountVectorizer(); m=v.fit_transform(toy)
print(pd.DataFrame(m.todense(),columns=v.get_feature_names_out()))

Xtr,Xte,ytr,yte=train_test_split(df.texto_limpio,df.tema,test_size=0.25,random_state=0,stratify=df.tema)
vec=TfidfVectorizer(lowercase=True,min_df=2,max_df=0.95)
A=vec.fit_transform(Xtr); B=vec.transform(Xte)
base=DummyClassifier(strategy="most_frequent").fit(A,ytr)
mod=LogisticRegression(max_iter=1000,random_state=0).fit(A,ytr)
print("n",len(df),"vocab",A.shape[1])
print("baseline",round(base.score(B,yte),2),"modelo",round(mod.score(B,yte),2))
tok=vec.get_feature_names_out()
for i,c in enumerate(mod.classes_):
    top=sorted(zip(mod.coef_[i],tok))[-5:][::-1]
    print(c,[t for _,t in top])
for t in ["Las exportaciones de camarón sumaron 3.253,37 millones de USD.","El desempleo bajó en el trimestre.","El club ganó el partido de ayer por dos goles.","Se aprobó el presupuesto de la institución para el próximo año."]:
    p=mod.predict_proba(vec.transform([preprocess(t)]))[0]
    print(round(p.max(),2),mod.classes_[p.argmax()],"|",t)

# confianza a mano
import numpy as np
x=vec.transform([preprocess("Las exportaciones de camarón sumaron 3.253,37 millones de USD.")])
z=x.toarray()[0]@mod.coef_.T+mod.intercept_
print("puntajes z",dict(zip(mod.classes_,z.round(2))))
p=np.exp(z)/np.exp(z).sum()
print("softmax a mano",p.round(2),"| predict_proba",mod.predict_proba(x)[0].round(2))
