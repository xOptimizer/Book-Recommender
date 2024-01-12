from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Define file paths for pickled data
POPULAR_FILE = 'popular.pkl'
PT_FILE = 'pt.pkl'
BOOKS_FILE = 'books.pkl'
SIMILARITY_SCORES_FILE = 'similarity_scores.pkl'

popular_df = pickle.load(open(POPULAR_FILE, 'rb'))
pt = pickle.load(open(PT_FILE, 'rb'))
books = pickle.load(open(BOOKS_FILE, 'rb'))
similarity_scores = pickle.load(open(SIMILARITY_SCORES_FILE, 'rb'))


@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_ratings'].values)
                           )


@app.route('/recommender')
def recommender_ui():
    return render_template('recommender.html')


@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    try:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

            data.append(item)

        print(data)

        return render_template('recommender.html', data=data)
    except IndexError:
        error_message = "Book not found. Please enter a valid book title."
        return render_template('recommender.html', error_message=error_message)


@app.route('/about')
def about_ui():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
