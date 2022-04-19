import numpy as np

from bokeh.layouts import column, row
from bokeh.models import CustomJS, Slider
from bokeh.plotting import ColumnDataSource, figure, show

x = [0, 0.5]
y = [0.5, 0]
ref_x = [0.2, 0.11666, 0.1]
ref_y = [0.2, 0.11666, 0.1]
gline = ColumnDataSource(data=dict(x=x, y=y))
payments = ColumnDataSource(data=dict(x=ref_x, y=ref_y))
legs = ["test1", "test2"]
plot = figure(y_range=(0, 1), x_range=(0, 1), width=400, height=400, title="e_BNE_Calculator")

# G line
plot.line('x', 'y', source=gline, line_width=3, line_alpha=0.6)
# payments
plot.circle('x', 'y', source=payments)

A_Value = Slider(start=0, end=1, value=0.3, step=.01, title="A_Value")
B_Value = Slider(start=0, end=1, value=0.3, step=.01, title="B_Value")
G_Value = Slider(start=0, end=2, value=0.5, step=.01, title="G_Value")


callback = CustomJS(args=dict(payments=payments, gline=gline, aval=A_Value, bval=B_Value, gval=G_Value),
                    code="""
    function payment_vcg(a, b, g) {
    if ( g > a + b ) {
        return [0, 0, a+b];
    } else {
        return [Math.max(0, -b+g), Math.max(0, -a+g), 0];
    }
    }
    
    const A = aval.value;
    const B = bval.value;
    const G = gval.value;
    const line = gline.data;
    const x = line['x']
    const y = line['y']
    y[0] = G;
    x[1] = G;
    gline.change.emit();
    const data = payments.data;
    const x1 = data['x']
    const y1 = data['y']
    const TMP = payment_vcg(A, B, G);
    x1[0] = TMP[0];
    y1[0] = TMP[1];
    x1[1] = A / 6 - B/3 + G/3;
    y1[1] = B / 6 - A/3 + G/3;
    x1[2] = TMP[0]/2;
    y1[2] = TMP[1]/2;
    payments.change.emit();
""")

'''
const data2 = payments.data;
const x1 = data2['x']
const y1 = data2['y']
x1[0] = G - B;
y1[0] = G - A;
x1[1] = A / 6 - B/3 + G/3;
y1[2] = B / 6 - A/3 + G/3;
payments.change.emit();
'''
A_Value.js_on_change('value', callback)
B_Value.js_on_change('value', callback)
G_Value.js_on_change('value', callback)

layout = row(
    plot,
    column(A_Value, B_Value, G_Value),
)

show(layout)