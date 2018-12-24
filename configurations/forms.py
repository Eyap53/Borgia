from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class ConfigurationCenterForm(forms.Form):
    center_name = forms.CharField(label='Nom du centre Borgia', max_length=255)


class ConfigurationProfitForm(forms.Form):
    margin_profit = forms.DecimalField(label='Marge appliquée aux prix en mode automatique (%)',
                                       decimal_places=2, max_digits=9,
                                       validators=[
                                           MinValueValidator(0, 'Le montant doit être positif')])


class ConfigurationLydiaForm(forms.Form):
    lydia_min_price = forms.DecimalField(label='Montant minimal de rechargement (€)',
                                         decimal_places=2, max_digits=9,
                                         validators=[
                                             MinValueValidator(0, 'Le montant doit être positif')],
                                         required=False)
    lydia_max_price = forms.DecimalField(label='Montant maximal de rechargement (€)',
                                         decimal_places=2, max_digits=9,
                                         validators=[
                                             MinValueValidator(0, 'Le montant doit être positif')],
                                         required=False)
    lydia_api_token = forms.CharField(label='Clé API (privée)', max_length=255)
    lydia_vendor_token = forms.CharField(
        label='Clé vendeur (publique)', max_length=255)

    def clean(self):
        """
        If min and max:
            max >= min
        """
        cleaned_data = super().clean()
        lydia_min_price = cleaned_data.get("lydia_min_price", None)
        lydia_max_price = cleaned_data.get("lydia_max_price", None)
        if lydia_min_price is not None and lydia_max_price is not None:
            if lydia_max_price < lydia_min_price:
                raise ValidationError(
                    "Le montant maximal doit être supérieur ou égal au montant minimal")


class ConfigurationBalanceForm(forms.Form):
    balance_threshold_purchase = forms.DecimalField(label='Valeur seuil (€) pour pouvoir acheter',
                                                    decimal_places=2, max_digits=9)
    """
    balance_threshold_mail_alert = forms.DecimalField(label='Valeur seuil (€) de l\'alerte par email',
                                        decimal_places=2, max_digits=9,
                                        required=False)
    balance_frequency_mail_alert = forms.IntegerField(label='Fréquence de l\'alerte par email',
                                        validators=[
                                          MinValueValidator(1, 'La fréquence doit être d\'au moins 1 jour')],
                                        required=False)
    """