menu_text = ("🛒 Магазин\n\n"
             "💰 Кэшбэк: *0$*"
             "\n💲 Ваша скидка: *0%* и *0$*")


magazine_text = ("🧾 *Формирование заказа*\n\n"
                 "Выберите, пожалуйста, город, в котором желаете приобрести товар:")

geo_text = ("🧾 *Формирование заказа*\n\n"
            "Выберите, пожалуйста, товар, который желаете приобрести:")

payment_text = ("🧾 *Формирование заказа*\n\n"
                "🏙 *Локация*: `{geo}`\n"
                "📦 *Товар*: `{product}`\n\n"
                "Выберите, пожалуйста, наиболее удобный для Вас способ оплаты:")

confirm_text = ("🧾 *Подтверждение заказа*\n\n"
                "🏙 *Локация*: `{geo}`\n"
                "📦 *Товар*: {product} {gram}\n\n"
                "💎 *Способ оплаты*: LiteCoin\n\n"
                "💲 *Стоимость*: {price}$\n"
                "├ *Скидка на товар*: 0%\n"
                "├ *Ваши скидки*: 0% и 0$\n"
                "├ *Кэшбэк за предыдущие покупки*: 0$\n"
                "└ *Итого к оплате*: {price}$\n\n\n"
                "_При выдаче реквизитов для оплаты сумма может повыситься, так как обменники берут дополнительную комиссию за обработку операций_.\n\n"
                "Если Вас все устраивает, подтвердите создание заказа:")


order_text = ("🛒 *Заказ* #{order_id}\n\n"
              "Оплатите, пожалуйста, заказ по данным реквизитам:\n"
              "👛 *Кошелек*: `{req}`\n"
              "_Нажмите на кошелек, чтобы скопировать_\n"
              "💲 *Сумма для перевода*: `{ltc_sum}` *LTC*\n"
              "_Нажмите на сумму, чтобы скопировать_\n\n\n"
              "*У вас есть 20 минут на оплату заявки, далее она отменится автоматически."
              "Переводите точную сумму, в случае ошибки, заказ не будет выдан, а средства невозможно будет вернуть*.")

confirm_cancel = ("🔐 *Подтверждение отмены*\n\n"
                  "Вы уверены, что хотите отменить заявку?\n\n"
                  "‼️*Пожалуйста, убедитесь, что вы не оплачивали, в случае отмены, возврат средств и повторная проверка оплаты будет невозможна*.")


confirm_cancel_now = ("🔐 *Подтверждение отмены*\n\n"
                      "Вы уверены, что хотите отменить заявку?\n\n"
                      "‼️*Пожалуйста, убедитесь, что вы не оплачивали, в случае отмены, возврат средств и повторная проверка оплаты будет невозможна*.")


invoice_canceled = ("🔴 *Заявка отменена*\n\n"
                    "Ваша заявка был успешно отменена. В случае повторных множественных отмен, Ваш аккаунт будет заблокирован.")

pokupka_text = ("🛍 Номер #{num}\n\n"
                "🏙 Локация: {geo}\n"
                "📦 Товар: `{product_name}`\n\n"
                "💎 Способ оплаты: LTC\n\n"
                "📩 Полученный адрес:\n `{adr}`")

promo_text = ("🏷 *Промокод*\n\n"
              "Здесь вы можете активировать промокод, который получили от администрации магазина, он может выдать Вам скидку в числовом или процентном эквиваленте.")

ref_text = ("👥 *Реферальная программа*\n\n"
            "Ваша реферальная ссылка:  `t.me/{bot}?start=65d51f42d2e7e4912c21aeb6db2f4f0a`\n"
            "Привлечено пользователей: *0*\n\n"
            "Привлекайте пользователей в наш бот и зарабатывайте *0%* от всех их покупок на свой внутренней баланс магазина, и получайте товар бесплатно!")

