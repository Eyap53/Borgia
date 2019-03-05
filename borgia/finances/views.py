#-*- coding: utf-8 -*-
import datetime
import decimal
import hashlib
import operator

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db.models import Q
from django.http import Http404
from django.shortcuts import HttpResponse, render
from django.urls import reverse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt

from borgia.views import BorgiaFormView, BorgiaView
from configurations.models import Configuration
from configurations.utils import configurations_get
from finances.forms import (ExceptionnalMovementForm,
                            GenericListSearchDateForm, RechargingCreateForm,
                            RechargingListForm, SelfLydiaCreateForm,
                            TransfertCreateForm)
from finances.models import (Cash, Cheque, ExceptionnalMovement, Lydia,
                             Recharging, Transfert)
from users.mixins import UserMixin
from users.models import User


class RechargingList(LoginRequiredMixin, PermissionRequiredMixin, BorgiaFormView):
    """
    View to list recharging sales.

    The view handle request of the form to filter recharging sales.
    :note:: only recharging sales are listed here. For other types of
    transactions, please refer to other classes (SaleList, TransfertList and
    ExceptionnalMovementList).
    """
    permission_required = 'finances.view_recharging'
    menu_type = 'managers'
    template_name = 'finances/recharging_list.html'
    form_class = RechargingListForm
    lm_active = 'lm_recharging_list'

    search = None
    date_end = now() + datetime.timedelta(days=1)
    date_begin = now() - datetime.timedelta(days=7)
    operators = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['recharging_list'] = self.form_query(
            Recharging.objects.all().order_by(
                '-datetime'))[:1000]

        context['info'] = self.info(context['recharging_list'])
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['date_begin'] = self.date_begin
        initial['date_end'] = self.date_end
        return initial

    def info(self, query):
        info = {
            'cash': {
                'total': 0,
                'nb': 0,
                'ids': []
            },
            'cheque': {
                'total': 0,
                'nb': 0,
                'ids': []
            },
            'lydia_face2face': {
                'total': 0,
                'nb': 0,
                'ids': []
            },
            'lydia_online': {
                'total': 0,
                'nb': 0,
                'ids': []
            },
            'total': {
                'total': 0,
                'nb': 0
            }
        }

        for recharging in query:
            if recharging.content_solution.__class__.__name__ == 'Cash':
                info['cash']['total'] += recharging.content_solution.amount
                info['cash']['nb'] += 1
                info['cash']['ids'].append(recharging.content_solution)
            elif recharging.content_solution.__class__.__name__ == 'Cheque':
                info['cheque']['total'] += recharging.content_solution.amount
                info['cheque']['nb'] += 1
                info['cheque']['ids'].append(recharging.content_solution)
            elif recharging.content_solution.__class__.__name__ == 'Lydia':
                if recharging.content_solution.is_online is False:
                    info['lydia_face2face']['total'] += recharging.content_solution.amount
                    info['lydia_face2face']['nb'] += 1
                    info['lydia_face2face']['ids'].append(recharging.content_solution)
                else:
                    info['lydia_online']['total'] += recharging.content_solution.amount
                    info['lydia_online']['nb'] += 1
                    info['lydia_online']['ids'].append(recharging.content_solution)
            info['total']['total'] += recharging.content_solution.amount
            info['total']['nb'] += 1
        return info

    def form_query(self, query):
        if self.search:
            query = query.filter(
                Q(operator__last_name__contains=self.search)
                | Q(operator__first_name__contains=self.search)
                | Q(operator__surname__contains=self.search)
                | Q(sender__last_name__contains=self.search)
                | Q(sender__first_name__contains=self.search)
                | Q(sender__surname__contains=self.search)
            )

        if self.date_begin:
            query = query.filter(
                datetime__gte=self.date_begin)

        if self.date_end:
            query = query.filter(
                datetime__lte=self.date_end)

        if self.operators:
            query = query.filter(operator__in=self.operators)

        return query

    def form_valid(self, form):
        if form.cleaned_data['search'] != '':
            self.search = form.cleaned_data['search']

        if form.cleaned_data['date_begin'] != '':
            self.date_begin = form.cleaned_data['date_begin']

        if form.cleaned_data['date_end'] != '':
            self.date_end = form.cleaned_data['date_end']

        if form.cleaned_data['operators']:
            self.operators = form.cleaned_data['operators']

        return self.get(self.request, self.args, self.kwargs)


class RechargingRetrieve(LoginRequiredMixin, PermissionRequiredMixin, BorgiaView):
    """
    Retrieve a recharging sale.

    For other type of transaction, please refer to other classes (SaleRetrieve,
    TransfertRetrieve, ExceptionnalMovementRetrieve).
    """
    permission_required = 'finances.view_recharging'
    menu_type = 'managers'
    template_name = 'finances/recharging_retrieve.html'

    def __init__(self):
        self.recharging = None

    def add_recharging_object(self):
        """
        Define shop object.
        Raise Http404 is shop doesn't exist.
        """
        try:
            self.recharging = Recharging.objects.get(
                pk=self.kwargs['recharging_pk'])
        except ObjectDoesNotExist:
            raise Http404

    def has_permission(self):
        has_perms = super().has_permission()
        if not has_perms:
            return False
        else:
            self.add_recharging_object()
            return True

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['recharging'] = self.recharging
        return render(request, self.template_name, context=context)


class TransfertList(LoginRequiredMixin, PermissionRequiredMixin, BorgiaFormView):
    """
    View to list transfert sales.

    The view handle request of the form to filter transfert sales.
    :note:: only transfert sales are listed here. For other types of
    transactions, please refer to other classes (SaleList, RechargingList and
    ExceptionnalMovementList).
    """
    permission_required = 'finances.view_transfert'
    menu_type = 'managers'
    template_name = 'finances/transfert_list.html'
    form_class = GenericListSearchDateForm
    lm_active = 'lm_transfert_list'

    search = None
    date_begin = None
    date_end = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['transfert_list'] = self.form_query(
            Transfert.objects.all().order_by('-datetime')
        )[:100]

        return context

    def form_query(self, query):
        if self.search:
            query = query.filter(
                Q(recipient__last_name__contains=self.search)
                | Q(recipient__first_name__contains=self.search)
                | Q(recipient__surname__contains=self.search)
                | Q(sender__last_name__contains=self.search)
                | Q(sender__first_name__contains=self.search)
                | Q(sender__surname__contains=self.search)
            )

        if self.date_begin:
            query = query.filter(
                datetime__gte=self.date_begin)

        if self.date_end:
            query = query.filter(
                datetime__lte=self.date_end)

        return query

    def form_valid(self, form):
        if form.cleaned_data['search'] != '':
            self.search = form.cleaned_data['search']

        if form.cleaned_data['date_begin'] != '':
            self.date_begin = form.cleaned_data['date_begin']

        if form.cleaned_data['date_end'] != '':
            self.date_end = form.cleaned_data['date_end']

        return self.get(self.request, self.args, self.kwargs)


class TransfertRetrieve(LoginRequiredMixin, PermissionRequiredMixin, BorgiaView):
    """
    Retrieve a transfert sale.

    For other type of transaction, please refer to other classes (SaleRetrieve,
    RechargingRetrieve, ExceptionnalMovementRetrieve).

    """
    permission_required = 'finances.view_transfert'
    menu_type = 'managers'
    template_name = 'finances/transfert_retrieve.html'

    def __init__(self):
        self.transfert = None

    def add_transfert_object(self):
        """
        Define shop object.
        Raise Http404 is shop doesn't exist.
        """
        try:
            self.transfert = Transfert.objects.get(
                pk=self.kwargs['transfert_pk'])
        except ObjectDoesNotExist:
            raise Http404

    def has_permission(self):
        has_perms = super().has_permission()
        if not has_perms:
            return False
        else:
            self.add_transfert_object()
            return True

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['transfert'] = self.transfert
        return render(request, self.template_name, context=context)


class TransfertCreate(LoginRequiredMixin, PermissionRequiredMixin, BorgiaFormView):
    permission_required = 'finances.add_transfert'
    menu_type = 'members'
    success_message = "Le montant de %(amount)s€ a bien été transféré à %(recipient)s."
    template_name = 'finances/transfert_create.html'
    form_class = TransfertCreateForm
    lm_active = 'lm_transfert_create'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['sender'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Get user or ValidationError
        recipient = form.cleaned_data['recipient']

        transfert = Transfert.objects.create(
            sender=self.request.user,
            recipient=recipient,
            amount=form.cleaned_data['amount'],
            justification=form.cleaned_data['justification']
        )
        transfert.pay()
        return super(TransfertCreate, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            amount=cleaned_data['amount'],
            recipient=cleaned_data['recipient']
        )

    def get_success_url(self):
        return reverse('url_members_workboard')


class ExceptionnalMovementList(LoginRequiredMixin, PermissionRequiredMixin, BorgiaFormView):
    """
    View to list exceptionnal movement sales.

    The view handle request of the form to filter recharging exceptionnal
    movement.
    :note:: only exceptionnal movement sales are listed here. For other types
    of transactions, please refer to other classes (SaleList, TransfertList and
    SaleList).

    """
    permission_required = 'finances.view_exceptionnalmovement'
    menu_type = 'managers'
    template_name = 'finances/exceptionnalmovement_list.html'
    form_class = GenericListSearchDateForm
    lm_active = 'lm_exceptionnalmovement_list'

    search = None
    date_begin = None
    date_end = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exceptionnalmovement_list'] = self.form_query(
            ExceptionnalMovement.objects.all().order_by('-datetime')
        )[:100]
        return context

    def form_query(self, query):
        if self.search:
            query = query.filter(
                Q(operator__last_name__contains=self.search)
                | Q(operator__first_name__contains=self.search)
                | Q(operator__surname__contains=self.search)
                | Q(recipient__last_name__contains=self.search)
                | Q(recipient__first_name__contains=self.search)
                | Q(recipient__surname__contains=self.search)
            )

        if self.date_begin:
            query = query.filter(
                datetime__gte=self.date_begin)

        if self.date_end:
            query = query.filter(
                datetime__lte=self.date_end)

        return query

    def form_valid(self, form):
        if form.cleaned_data['search'] != '':
            self.search = form.cleaned_data['search']

        if form.cleaned_data['date_begin'] != '':
            self.date_begin = form.cleaned_data['date_begin']

        if form.cleaned_data['date_end'] != '':
            self.date_end = form.cleaned_data['date_end']

        return self.get(self.request, self.args, self.kwargs)


class ExceptionnalMovementRetrieve(LoginRequiredMixin, PermissionRequiredMixin, BorgiaView):
    """
    Retrieve an exceptionnal movement sale.

    For other type of transaction, please refer to other classes (SaleRetrieve,
    TransfertRetrieve, RechargingRetrieve).
    """
    permission_required = 'finances.view_exceptionnalmovement'
    menu_type = 'managers'
    template_name = 'finances/exceptionnalmovement_retrieve.html'

    def __init__(self):
        self.exceptionnalmovement = None

    def add_exceptionnalmovement_object(self):
        """
        Define shop object.
        Raise Http404 is shop doesn't exist.
        """
        try:
            self.exceptionnalmovement = ExceptionnalMovement.objects.get(
                pk=self.kwargs['exceptionnalmovement_pk'])
        except ObjectDoesNotExist:
            raise Http404

    def has_permission(self):
        has_perms = super().has_permission()
        if not has_perms:
            return False
        else:
            self.add_exceptionnalmovement_object()
            return True

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['exceptionnalmovement'] = self.exceptionnalmovement
        return render(request, self.template_name, context=context)


class SelfTransactionList(LoginRequiredMixin, BorgiaFormView):
    """
    View to list transactions of the logged user.
    """
    menu_type = 'members'
    template_name = 'finances/self_transaction_list.html'
    form_class = GenericListSearchDateForm
    lm_active = 'lm_self_transaction_list'

    search = None
    date_begin = None
    date_end = None

    def get_context_data(self, **kwargs):
        context = super(SelfTransactionList, self).get_context_data(**kwargs)
        context['transaction_list'] = self.form_query(
            self.request.user.list_transaction())[:100]
        return context

    # TODO: form to be used
    def form_query(self, query):
        return query

    def form_valid(self, form):
        if form.cleaned_data['search']:
            self.search = form.cleaned_data['search']
        if form.cleaned_data['date_begin']:
            self.date_begin = form.cleaned_data['date_begin']

        if form.cleaned_data['date_end']:
            self.date_end = form.cleaned_data['date_end']
        try:
            if form.cleaned_data['shop']:
                self.query_shop = form.cleaned_data['shop']
        except KeyError:
            pass
        return self.get(self.request, self.args, self.kwargs)


class UserExceptionnalMovementCreate(UserMixin, BorgiaFormView):
    """
    View to create an exceptionnal movement (debit or credit) for a specific
    user.
    """
    permission_required = 'finances.add_exceptionnalmovement'
    menu_type = 'managers'
    template_name = 'finances/user_exceptionnalmovement_create.html'
    form_class = ExceptionnalMovementForm
    lm_active = None

    def form_valid(self, form):
        """
        :note:: The form is assumed clean, then the couple username/password
        for the operator is right.
        """
        operator = authenticate(
            username=form.cleaned_data['operator_username'],
            password=form.cleaned_data['operator_password'])
        amount = form.cleaned_data['amount']
        is_credit = False

        if form.cleaned_data['type_movement'] == 'credit':
            is_credit = True

        exceptionnal_movement = ExceptionnalMovement.objects.create(
            justification=form.cleaned_data['justification'],
            operator=operator,
            recipient=self.user,
            is_credit=is_credit,
            amount=amount
        )
        exceptionnal_movement.pay()

        return super().form_valid(form)

    def get_initial(self):
        """
        Populate the form with the current login user for the operator (only
        username of course).
        """
        initial = super().get_initial()
        initial['operator_username'] = self.request.user.username
        return initial

    def get_success_url(self):
        return reverse('url_user_retrieve', kwargs={'user_pk': self.user.pk})


class RechargingCreate(UserMixin, BorgiaFormView):
    permission_required = 'finances.add_recharging'
    menu_type = 'managers'
    template_name = 'finances/user_supplymoney.html'
    form_class = RechargingCreateForm
    lm_active = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        """
        :note:: The form is assumed clean, then the couple username/password
        for the operator is right.
        """
        operator = authenticate(
            username=form.cleaned_data['operator_username'],
            password=form.cleaned_data['operator_password'])
        sender = self.user

        if form.cleaned_data['type'] == 'cheque':
            recharging_solution = Cheque.objects.create(
                amount=form.cleaned_data['amount'],
                signature_date=form.cleaned_data['signature_date'],
                cheque_number=form.cleaned_data['unique_number'],
                sender=sender)

        elif form.cleaned_data['type'] == 'cash':
            recharging_solution = Cash.objects.create(
                sender=sender,
                amount=form.cleaned_data['amount'])

        elif form.cleaned_data['type'] == 'lydia':
            recharging_solution = Lydia.objects.create(
                sender=sender,
                amount=form.cleaned_data['amount'],
                date_operation=form.cleaned_data['signature_date'],
                id_from_lydia=form.cleaned_data['unique_number'],
                is_online=False)

        recharging = Recharging.objects.create(
            sender=sender,
            operator=operator,
            content_solution=recharging_solution
        )
        recharging.pay()

        return super().form_valid(form)

    def get_initial(self):
        """
        Populate the form with the current login user for the operator (only
        username of course).
        """
        initial = super().get_initial()
        initial['signature_date'] = now
        initial['operator_username'] = self.request.user.username
        return initial

    def get_success_url(self):
        return reverse('url_user_retrieve', kwargs={'user_pk': self.user.pk})


class SelfLydiaCreate(LoginRequiredMixin, BorgiaFormView):
    """
    View to supply himself by Lydia.
    """
    menu_type = 'members'
    template_name = 'finances/self_lydia_create.html'
    form_class = SelfLydiaCreateForm
    lm_active = 'lm_self_lydia_create'

    def get_form_kwargs(self):
        kwargs = super(SelfLydiaCreate, self).get_form_kwargs()

        # Min value is always 0.01
        try:
            min_value = Configuration.objects.get(
                name='LYDIA_MIN_PRICE').get_value()
            if min_value is not None:
                if min_value > 0:
                    kwargs['min_value'] = decimal.Decimal(min_value)
                else:
                    kwargs['min_value'] = decimal.Decimal("0.01")
            else:
                kwargs['min_value'] = decimal.Decimal("0.01")
        except ObjectDoesNotExist:
            kwargs['min_value'] = decimal.Decimal("0.01")

        try:
            max_value = Configuration.objects.get(
                name='LYDIA_MAX_PRICE').get_value()
            if max_value is not None:
                kwargs['max_value'] = decimal.Decimal(max_value)
            else:
                kwargs['max_value'] = None
        except ObjectDoesNotExist:
            kwargs['max_value'] = None

        return kwargs

    def form_valid(self, form):
        """
        Save the current phone number as default phone number for the user.
        Render the Lydia button.
        """
        user = self.request.user
        if user.phone is None:
            user.phone = form.cleaned_data['tel_number']
            user.save()

        context = super().get_context_data()
        context['vendor_token'] = configurations_get(
            "LYDIA_VENDOR_TOKEN").get_value()
        context['confirm_url'] = settings.LYDIA_CONFIRM_URL
        context['callback_url'] = settings.LYDIA_CALLBACK_URL
        context['amount'] = form.cleaned_data['amount']
        context['tel_number'] = form.cleaned_data['tel_number']
        context['message'] = (
            "Borgia - AE ENSAM - Crédit de "
            + user.__str__())
        return render(self.request,
                      'finances/self_lydia_button.html',
                      context=context)

    def get_initial(self):
        initial = super().get_initial()
        initial['tel_number'] = self.request.user.phone
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            if configurations_get("LYDIA_API_TOKEN").get_value() in ['', 'non définie']:
                context['no_module'] = True
            else:
                context['no_module'] = False
        except:
            context['no_module'] = True
        return context


class SelfLydiaConfirm(LoginRequiredMixin, BorgiaView):
    """
    View to confirm supply by Lydia.

    This view is only here to have some indications for the user. It does
    nothing more and can be "generated" with GET irelevant GET parameters.

    :note:: transaction and order parameters are given by Lydia but aren't
    used here.
    """
    menu_type = 'members'
    template_name = 'finances/self_lydia_confirm.html'

    # TODO: check if a Lydia object exist and if it's from the current day,
    # else raise Error
    def get(self, request, *args, **kwargs):
        context = super().get_context_data()
        context['transaction'] = self.request.GET.get('transaction')
        context['order'] = self.request.GET.get('order_ref')
        return render(request, self.template_name, context=context)


@csrf_exempt
@login_required
def self_lydia_callback(request):
    """
    Function to catch the callback from Lydia after a payment.

    Create all objects needed to have a proper sale in the database, and credit
    the client.

    :param GET['user_pk']: pk of the client, mandatory.
    :param POST['currency']: icon of the currency, for instance EUR, mandatory.
    :param POST['request_id']: request id from lydia, mandatory.
    :param POST['amount']: amount of the transaction, in 'currency', mandatory.
    :param POST['signed']: internal to Lydia ?
    :param POST['transaction_identifier']: transaction id from Lydia,
    mandatory.
    :param POST['vendor_token']: public key of the association, mandatory.
    :param POST['sig']: signatory generated by Lydia to identify the
    transaction, mandator.
    :type GET['user_pk']: positiv integer
    :type POST['currency']: string
    :type POST['request_id: string
    :type POST['amount']: float (decimal)
    :type POST['signed']: boolean
    :type POST['transaction_identifier']: string
    :type POST['vendor_token']: string
    :type POST['sig']: string

    :note:: Even if some parameters tend to be useless (signed, request_id),
    they are mandatory because used to generated the signatory and verify the
    transaction.

    :raises: PermissionDenied if signatory generated is not sig.
    :returns: 300 if the user_pk doesn't match an user.
    :returns: 300 if a parameter is missing.
    :returns: 200 if all's good.
    :rtype: Http request
    """
    params_dict = {
        "currency": request.POST.get("currency"),
        "request_id": request.POST.get("request_id"),
        "amount": request.POST.get("amount"),
        "signed": request.POST.get("signed"),
        "transaction_identifier": request.POST.get("transaction_identifier"),
        "vendor_token": request.POST.get("vendor_token"),
        "sig": request.POST.get("sig")
    }
    lydia_token = configurations_get("LYDIA_API_TOKEN").get_value()
    if verify_token_algo_lydia(params_dict, lydia_token) is True:
        try:
            user = User.objects.get(pk=request.GET.get('user_pk'))
            lydia = Lydia.objects.create(
                sender=user,
                amount=decimal.Decimal(params_dict['amount']),
                id_from_lydia=params_dict['transaction_identifier']
            )
            recharging = Recharging.objects.create(
                sender=user,
                operator=user,
                content_solution=lydia
            )
            recharging.pay()
        except KeyError:
            return HttpResponse('300')
        except ObjectDoesNotExist:
            return HttpResponse('300')
        return HttpResponse('200')
    else:
        raise PermissionDenied


def verify_token_algo_lydia(params, token):
    """
    Verify request parameters according to Lydia's algorithm.

    If parameters are valid, the request is authenticated to be from Lydia and
    can be safely used.
    :note:: sig must be contained in the parameters dictionary.

    :warning:: token is private and must never be revealed.

    :param params: all parameters, including sig, mandatory.
    :type params: python dictionary
    :param token: token to be compared, mandatory.
    :type token: string

    :returns: True if parameters are valid, False else.
    :rtype: Boolean
    """
    try:
        sig = params['sig']
        del params['sig']
        h_sig_table = []
        sorted_params = sorted(params.items(), key=operator.itemgetter(0))
        for param in sorted_params:
            h_sig_table.append(param[0] + '=' + param[1])
        h_sig = '&'.join(h_sig_table)
        h_sig += '&' + token
        h_sig_hash = hashlib.md5(h_sig.encode())
        return h_sig_hash.hexdigest() == sig

    except KeyError:
        return False