from bot import TOKEN



URL_INFO = f'https://api.telegram.org/bot{TOKEN}/getFile?file_id='
URL = f'https://api.telegram.org/file/bot{TOKEN}/'

START_COMMAND = '''
<b>Добро пожаловать в бот.🖐🖐🖐</b>

Этот бот дает возможность
обрабатывать фото несколькими
фильтрами и изменять размер
вашего изображения.

<b>Загрузите желаемое изображение...</b>
'''
IMAGE_PROCESSING = '''
<b>Выберите тип обработки фото:</b>

<b>/black_white</b>   - <em>в черно-белое</em>
<b>/pencil</b>        - <em>в контур карандашом</em>
<b>/marble</b>        - <em>эффект мрамора</em>
<b>/coal</b>          - <em>рисунок углем</em>
<b>/exotic_pencil</b> - <em>экзотический карандаш</em>
<b>/paper_deep</b>    - <em>глубокая калька</em>
<b>/paper</b>         - <em>калька</em>
<b>/resize</b>        - <em>изменить размер фото</em>
<b>/cancel</b>       - <em>отмена</em>
'''

RESIZE_COMMAND = '''
<b>Введите процент увеличения или уменьшения фото.
Увеличение не более 150%</b>
<em>Пример:</em>
увеличение на 50%, написать      <b>+50</b>
уменьшение на 73%, написать      <b>-73</b>
'''