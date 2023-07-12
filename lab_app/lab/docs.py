POST_METHOD_DOCS = {
  'summary': 'Inserts information in database through endpoint',
  'description': 'Allows to insert information especified in request body in database.',
    # 'request': {
    #     'type': 'object',
    #     'properties': {
    #         'name': {
    #             'type': 'string',
    #             'description': 'Nombre del objeto'
    #         },
    #         'age': {
    #             'type': 'integer',
    #             'description': 'Edad del objeto'
    #         }
    #     },
    #     'required': ['name']
    # },
  'responses': {
      '201': {
          'description': 'Objeto creado exitosamente',
          'content': {
              'application/json': {
                  'schema': {
                      'type': 'object',
                      'properties': {
                          'id': {
                              'type': 'integer',
                              'description': 'ID del objeto creado'
                          },
                          'name': {
                              'type': 'string',
                              'description': 'Nombre del objeto creado'
                          },
                          'age': {
                              'type': 'integer',
                              'description': 'Edad del objeto creado'
                          }
                      }
                  }
              }
          }
      },
      '400': {
          'description': 'Solicitud inválida'
      }
  }
}

GET_METHOD_DOCS = {
  'summary': 'Obtain information from endpoint',
  'description': 'Allows to obtain information from endpoint.',
  'responses': {
    '200': {
      'description': 'Response success',
      'content': {
        'application/json': {
          'schema': {
            'type': 'object',
            'properties': {
              'id': {
                'type': 'integer',
                'description': 'ID del objeto'
              }
            }
          }
        }
      }
    },
    '404': {
        'description': 'No encontrado'
    }
  }
}

PUT_METHOD_DOCS = {
  'summary': 'Modifies information in database through endpoint',
  'description': 'Allows to update information in database via this endpoint.',
  'responses': {
      '200': {
          'description': 'Objeto actualizado exitosamente',
          'content': {
              'application/json': {
                  'schema': {
                      'type': 'object',
                      'properties': {
                          'id': {
                              'type': 'integer',
                              'description': 'ID del objeto actualizado'
                          },
                          'name': {
                              'type': 'string',
                              'description': 'Nuevo nombre del objeto'
                          },
                          'age': {
                              'type': 'integer',
                              'description': 'Nueva edad del objeto'
                          }
                      }
                  }
              }
          }
      },
      '400': {
          'description': 'Solicitud inválida'
      },
      '404': {
          'description': 'Objeto no encontrado'
      }
  }
}

DELETE_METHOD_DOCS = {
  'summary': 'Removes information in database through endpoint',
  'description': 'Allows to delete information in database via this endpoint.',
  'responses': {
      '204': {
          'description': 'Objeto eliminado exitosamente'
      },
      '400': {
          'description': 'Solicitud inválida'
      },
      '404': {
          'description': 'Objeto no encontrado'
      }
  }
}
