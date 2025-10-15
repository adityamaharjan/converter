from django import forms

# Only document formats for the target conversion
DOC_CHOICES = [
    ('pdf', 'PDF Document'),
    ('png', 'PNG Image'),
    # ('docx', 'Microsoft Word (DOCX)'),
    # ('odt', 'OpenDocument Text (ODT)'),

 
    # Add other document formats here
]

class FileConvertForm(forms.Form):
    # Field 1: The required file upload field
    input_file = forms.FileField(
        label='Select a file to upload',
        widget=forms.FileInput(attrs={'class': 'hidden-file-input', 'id': 'file-upload'}),
    )   
    
    # Field 2: What to convert to (Dropdown)
    convert_to = forms.ChoiceField(
    choices=DOC_CHOICES,
    label='Convert To Document Type',
    initial='pdf',
    widget=forms.Select(
        attrs={
            'class': 'mt-1 block w-lg mx-auto pl-3 pr-10 py-2 text-base border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white'
        }
    )
)