import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image


### モデル部分
model = tf.keras.models.load_model("src/saved_model.h5")


def sample_predict(img):
	'''画像に対して犬/猫の推論をする'''
	# 画像を160x160の正方形にする
	img = get_square_image(img)
	img = img.resize((160, 160))
	img_array = np.array(img)
	# 推論
	pred = tf.nn.sigmoid(model.predict(img_array[None, ...]))
	return 1 - pred.numpy()[0][0]  # 1に近いほど猫


def get_result(prediction):
	'''0-1の数値を受け取って表示用のテキストを返す'''
	if prediction < 0.05:
		result = "確実に犬"
	elif prediction < 0.2:
		result = "ほぼ犬"
	elif prediction < 0.5:
		result = "どちらかといえば犬"
	elif prediction < 0.8:
		result = "どちらかといえば猫"
	elif prediction < 0.95:
		result = "ほぼ猫"
	else:
		result = "確実に猫"
	return result


def get_square_image(target_img):
	'''画像に余白を加えて正方形にする'''
	bg_color = target_img.resize((1, 1)).getpixel((0, 0))  # 余白は全体の平均色
	width, height = target_img.size
	if width == height:
		return target_img
	elif width > height:
		resized_img = Image.new(target_img.mode, (width, width), bg_color)
		resized_img.paste(target_img, (0, (width - height) // 2))
		return resized_img
	else:
		resized_img = Image.new(target_img.mode, (height, height), bg_color)
		resized_img.paste(target_img, ((height - width) // 2, 0))
		return resized_img


### 表示部分
st.title("cat or dog ?")

uploaded_file = st.file_uploader("判定したい画像を選んでね")
if uploaded_file is not None:
	try:
		# 画像を読み込む
		uploaded_img = Image.open(uploaded_file)

		# 犬猫判定
		pred = sample_predict(uploaded_img)

		# 結果表示
		st.info(f"これは**{get_result(pred)}**です！")
		point = np.int(np.round(pred, 2)*20)
		st.text(f"犬 0 |{'-'*point}*{'-'*(19-point)}| 100 猫")
		st.image(uploaded_img, use_column_width=True)
	except:
		st.error("画像ファイルをアップロードしてください！")
