from django import forms
from .models import Question, Answer, Comment, ingredient_list

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content']
        labels = {
            'subject': '제목',
            'content': '내용',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }

class IngredientForm(forms.ModelForm):
    ingredient_choice = forms.ModelMultipleChoiceField(queryset=ingredient_list.objects.all()
                                                       , widget = forms.CheckboxSelectMultiple())
    
    class Meta:
        model = Question
        fields = ['ingredient']

    def save(self, commit=True):
        question = self.instance
        ingredient_list = '/'.join([qs.ingredient_list for qs in self.cleaned_data['ingredient_choice']])
        question.ingredient = ingredient_list
        question.save()

        return question
