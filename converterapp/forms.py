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
        label='Convert TO Document Type',
        initial='pdf',
    )