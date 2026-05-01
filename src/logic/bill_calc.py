def calculate_item(name,qty,price,gst_percent):
    q=float(qty)
    p=float(price)
    g=float(gst_percent)
    subtotal=q*p
    tax_amount=subtotal*(g/100)
    total=subtotal+tax_amount
    line_item_text=f"{name} | {q} x ₹{p} (+{g}% GST)=₹{round(total,2)} "
    return {
        "text":line_item_text,
        "Total":total
        
    }
    